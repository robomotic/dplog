# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from .views import (
    HomePageView,
    ClientView,EventView,
    QuestionVirtualCreate,
    QuestionVirtualView,
    QuestionCreate,
    QuestionView,
    simulation_view,
    simulation_run_view,
    sevice_status,
    list_questions,
    client_register
)

urlpatterns = [
    url(r"^$", HomePageView.as_view(), name="home"),
    # client information
    path('listClient', ClientView.as_view(), name='clients_list'),
    path('listEvents', EventView.as_view(), name='events_list'),
    # virtual surveys
    path('createVirtual', QuestionVirtualCreate.as_view(), name='questionvirtual_create'),
    path('listVirtual',QuestionVirtualView.as_view(), name='questionvirtual_list'),
    # real surveys
    path('create', QuestionCreate.as_view(), name='question_create'),
    path('list', QuestionView.as_view(), name='question_list'),
    # simulations
    path('runvirtualsim/<int:question_id>',simulation_run_view, name='runvirtualsim'),
    path('viewvirtualsim/<int:question_id>',simulation_view, name='viewvirtualsim'),
    # api for web client
    path('api/status',sevice_status, name='serverstatus'),
    path('api/client/register',csrf_exempt(client_register), name='registerclient'),
    path('api/questions/list',csrf_exempt(list_questions), name='listquestions'),

]