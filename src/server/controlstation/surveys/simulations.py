from .algorithms import MirroredQuestion
from .models import ClientVirtual,QuestionVirtual,ResponseVirtual,AggregateResponseVirtual
import math
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import random


def run_simulation(question):
    logger.info('Runing simulation for question {0}'.format(question.title))
    clients = [ClientVirtual(id=clientid) for clientid in range(1, question.total_clients + 1)]

    logger.info('Positive responses {0}'.format(question.positive_clients))
    for client in clients:
        client.save()
        # each client now provides a response
        responder = MirroredQuestion(p=question.params['p'], questions=[1, 0])
        if client.id <= question.positive_clients:
            # honest is a positive response
            choice = responder.respond(question=1)
            response = ResponseVirtual(question=question, client=client, count=choice)
        else:
            choice = responder.respond(question=0)
            response = ResponseVirtual(question=question, client=client, count=choice)

        response.save()
    # calculate the aggregated response
    # get all the responses from the question
    all_responses = question.responses.all()

    Z_1 = all_responses.filter(count__gte=1)
    logger.info('Positive observed responses {0}'.format(Z_1.count()))
    Z_0 = all_responses.filter(count__lt=1)

    logger.info('Negative observed responses {0}'.format(Z_0.count()))

    # sampling probability for positive questino
    p_y_1 = Z_1.count() / all_responses.count()

    print('Pr(Y = 1) = {0}'.format(p_y_1))

    p_z_1 = MirroredQuestion.estimate(question.params['p'], [1, 0], p_y_1, 1)

    Z_1_estimated = int(p_z_1 * all_responses.count())
    logger.info('Pr(Z = 1 ) = {0}'.format(p_z_1))
    logger.info('|Z = 1| = {0}'.format(Z_1_estimated))
    logger.info('|Y = 1| = {0}'.format(question.positive_clients))

    error = math.fabs(question.positive_clients - Z_1_estimated)
    logger.info('Error = {0}'.format(error))

    aggregated = AggregateResponseVirtual()
    aggregated.estimated_positive_clients = Z_1_estimated
    aggregated.estimated_positive_error = error

    aggregated.question = question
    aggregated.save()

    return aggregated

