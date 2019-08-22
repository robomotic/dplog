# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import QuestionVirtual,AggregateResponseVirtual
from .models import Client,ClientEvents
#from .forms import ContactForm, FilesForm, ContactFormSet
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseServerError
from .models import Client,Question
import json

from .simulations import run_simulation
from django.http import HttpResponse
from django.db.models import Sum


class HomePageView(TemplateView):
    template_name = "surveys/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context

class MiscView(TemplateView):
    template_name = "surveys/misc.html"

class QuestionVirtualCreate(CreateView):
    model = QuestionVirtual
    fields = ('title', 'observable','observable_type','max_rounds','total_clients','positive_clients','algorithm','params')

    success_url = reverse_lazy('home')

class QuestionCreate(CreateView):
    model = Question
    fields = ('title', 'observable','observable_type','max_rounds','begin_datetime','end_datetime','algorithm','params')

    success_url = reverse_lazy('home')

class QuestionVirtualView(ListView):

    model = QuestionVirtual
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ClientView(ListView):

    model = Client
    paginate_by = 10  # if pagination is desired
    ordering = ['guid']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventView(ListView):

    model = ClientEvents
    paginate_by = 10  # if pagination is desired
    ordering = ['-id']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class QuestionView(ListView):

    model = Question
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AggregateResponseVirtualView(DetailView):

    model = AggregateResponseVirtual
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def simulation_run_view(request, question_id):
    question = get_object_or_404(QuestionVirtual, pk=question_id)
    aggregated = run_simulation(question)
    if aggregated:
        question.completed = True
        question.save()

        responses = question.responses.all()

        real_positive = question.positive_clients
        real_negative = question.total_clients - real_positive

        private_positive = responses.aggregate(total_count=Sum('count'))['total_count']
        private_negative = question.total_clients - private_positive

        estimated_positive = aggregated.estimated_positive_clients
        estimated_negative = question.total_clients - estimated_positive

        return render(request, 'surveys/simulation_result.html', {'real':{'p':real_positive,'n':real_negative},
                                                                  'private':{'p':private_positive,'n':private_negative},
                                                                  'estimated': {'p': estimated_positive,
                                                                              'n': estimated_negative},'error':aggregated.estimated_positive_error})
    else:
        return HttpResponse(status=500)

def simulation_view(request, question_id):
    question = get_object_or_404(QuestionVirtual, pk=question_id)
    responses = question.responses.all()
    aggregated = question.aggregated.first()

    real_positive = question.positive_clients
    real_negative = question.total_clients - real_positive

    private_positive = responses.aggregate(total_count=Sum('count'))['total_count']
    private_negative = question.total_clients - private_positive

    estimated_positive = aggregated.estimated_positive_clients
    estimated_negative = question.total_clients - estimated_positive

    if aggregated:
        question.completed = True
        question.save()
        return render(request, 'surveys/simulation_result.html', {'real':{'p':real_positive,'n':real_negative},
                                                                  'private':{'p':private_positive,'n':private_negative},
                                                                  'estimated': {'p': estimated_positive,
                                                                              'n': estimated_negative},'error':aggregated.estimated_positive_error})
    else:
        return HttpResponse(status=500)

from .crypto import verify_signature
import os

class Config():
    def __init__(self,configuration='config.json'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path,configuration)
        with open(file_path) as config_file:
            data = json.load(config_file)

            self._secret = data["api-secret"].encode()


def sevice_status(request):
    banner = {'Version':0.9,'Up':1}
    return JsonResponse(banner, safe=False,status=200)

def list_questions(request):
    if request.method == 'GET':

        data = list(Question.objects.all().values())
        if "x-client-guid" in request.headers:
            # log this event
            event = ClientEvents(guid=request.headers["x-client-guid"], request_type='list/questions',
                                 response_type='ok')
            event.save()
            return JsonResponse(data, safe=False)
        else:
            # log this event
            event = ClientEvents(guid=request.headers["x-client-guid"], request_type='list/questions',
                                 response_type='denied missing client guid')
            event.save()
            return JsonResponse({'ack': False, 'error': 'Client GUID missing'}, safe=False, status=404)
    else:
        # log this event
        event = ClientEvents(guid=request.headers["x-client-guid"], request_type='list/questions',
                             response_type='denied method not allowed')
        event.save()
        return JsonResponse({'ack': False, 'error': 'Method not allowed'}, safe=False, status=404)

def client_register(request):
    if request.method == 'POST':

        if 'X-SIGNED' in request.headers:
            config = Config()
            verified = verify_signature(config._secret,request.body,request.headers['X-SIGNED'])

            if verified:
                json_data = json.loads(request.body)
                try:
                    guid = json_data['guid']
                    if Client.objects.filter(guid=guid):
                        oldclient = Client.objects.filter(guid=guid).first()
                        # log this event
                        event = ClientEvents(guid=guid,request_type='register',response_type='old')
                        event.save()

                        return JsonResponse({'ack': True, 'guid': guid, 'status':'Client was already registered on {0}'.format(oldclient.registered_datetime)}, safe=False)
                    else:
                        newclient = Client(guid=guid)
                        newclient.save()

                        # log this event
                        event = ClientEvents(guid=guid,request_type='register',response_type='new')
                        event.save()

                        return JsonResponse({'ack':True,'guid':guid,'status':'Client is now registered'}, safe=False)
                except KeyError:
                    return JsonResponse({'ack': False, 'error': 'Malformed request'}, safe=False,status=500)
            else:
                return JsonResponse({'ack': False, 'error': 'Signed request is not valid'}, safe=False, status=404)
        else:
            return JsonResponse({'ack': False, 'error': 'Request was not signed'}, safe=False, status=404)
    else:
        return JsonResponse({'ack': False, 'error': 'Method not allowed'}, safe=False,status=404)

