from django.test import TestCase
from .models import ClientVirtual,QuestionVirtual,ResponseVirtual
from .algorithms import MirroredQuestion
import math

import random

class TelemetryTestCase(TestCase):
    def setUp(self):
        random.seed(1)



# Create your tests here.
class SimulationRunTestCase(TestCase):
    def setUp(self):
        random.seed(1)

    def test_non_private_question(self,max_clients=10):
        """Test the honest response for 10 clients"""
        self.clients = [ClientVirtual(clientid) for clientid in range(1, max_clients + 1)]

        self.question = QuestionVirtual(title='Test question',
                                        observable='http://badwebsite.com',
                                        observable_type='D',
                                        algorithm='M')
        self.question.save()
        self.assertIsNotNone(self.question,msg='Unable to create virtual question')

        for positive_clients in range(0,max_clients+1):
            # clients with positive response
            for client in self.clients:
                # each client now provides a response
                if client.id <= positive_clients:
                    response = ResponseVirtual(question=self.question,client=client,count=1)
                else:
                    response = ResponseVirtual(question=self.question, client=client, count=0)

                response.save()
            # calculate the aggregated response
            # get all the responses from the question
            all_responses = self.question.responses.all()

            positive_check = all_responses.filter(count__gte=1)
            negative_check = all_responses.filter(count__lt=1)

            self.assertEqual(positive_check.count(),positive_clients)
            self.assertEqual(negative_check.count(),max_clients - positive_clients)

            #
            # now delete all previous responses
            self.question.responses.all().delete()

    def test_mirrored_question(self,max_clients=1000):
        """Test the mirrored questin design for 10 clients"""
        self.clients = [ClientVirtual(clientid) for clientid in range(1, max_clients + 1)]
        self.question = QuestionVirtual(title='Test question',
                                        observable='http://badwebsite.com',
                                        observable_type='D',
                                        algorithm='M')
        self.question.save()
        self.assertIsNotNone(self.question,msg='Unable to create virtual question')
        for p_choice in [0.8,0.9,0.95,0.99]:
            for positive_clients in [10,100,1000]:
                # clients with positive response
                print('Positive responses {0}'.format(positive_clients))
                for client in self.clients:
                    # each client now provides a response
                    responder = MirroredQuestion(p=p_choice,questions=[1,0])
                    if client.id <= positive_clients:
                        # honest is a positive response
                        choice = responder.respond(question=1)
                        response = ResponseVirtual(question=self.question,client=client,count=choice)
                    else:
                        choice = responder.respond(question=0)
                        response = ResponseVirtual(question=self.question, client=client, count=choice)

                    response.save()
                # calculate the aggregated response
                # get all the responses from the question
                all_responses = self.question.responses.all()

                Z_1 = all_responses.filter(count__gte=1)
                print('Positive observed responses {0}'.format(Z_1.count()))
                Z_0 = all_responses.filter(count__lt=1)

                print('Negative observed responses {0}'.format(Z_0.count()))

                # sampling probability for positive questino
                p_y_1 = Z_1.count() / all_responses.count()

                print('Pr(Y = 1) = {0}'.format(p_y_1))

                p_z_1 = MirroredQuestion.estimate(p_choice,[1,0],p_y_1,1)

                Z_1_estimated = int(p_z_1 * all_responses.count())
                print('Pr(Z = 1 ) = {0}'.format(p_z_1))
                print('|Z = 1| = {0}'.format(Z_1_estimated))
                print('|Y = 1| = {0}'.format(positive_clients))

                error = math.fabs(positive_clients - Z_1_estimated)
                print('Error = {0}'.format(error))
                if p_choice == 0.99:
                    self.assertLessEqual(error, 2.0)
                if p_choice == 0.95:
                    self.assertLessEqual(error, 11.0)
                if p_choice == 0.9:
                    self.assertLessEqual(error, 16.0)
                if p_choice == 0.8:
                    self.assertLessEqual(error, 33.0)

                # now delete all previous responses
                self.question.responses.all().delete()

    def tearDown(self):
        pass
