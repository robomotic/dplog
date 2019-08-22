#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...
"""

__author__ = "Dr. Paolo Di Prodi"
__copyright__ = "Copyright 2019, The Cogent Project"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Paolo Di Prodi"
__email__ = "paolo@logsotal.com"
__status__ = "Experimental"

import os
import json
import requests
import subprocess
import uuid
import hmac
import hashlib

from question import QuestionHandler


import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('client.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class BodyDigestSignature(object):
    def __init__(self, secret, header='X-SIGNED', algorithm=hashlib.sha512):
        self.secret = secret
        self.header = header
        self.algorithm = algorithm

    def __call__(self, request):
        body = request.body
        if not isinstance(body, bytes):   # Python 3
            body = body.encode('latin1')  # standard encoding for HTTP
        signature = hmac.new(self.secret, body, digestmod=self.algorithm)
        request.headers[self.header] = signature.hexdigest()
        return request

class ClientService():

    def __init__(self,configuration):

        with open(configuration) as config_file:
            data = json.load(config_file)

            if data['guid'] > 0:
                self._machineGuid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
            else:
                self._machineGuid = uuid.uuid1()

            self.url_sevice = 'http://'+data['server']+':'+str(data['port'])+'/api'
            self._secret = data["api-secret"].encode()

    def check_service(self):
        url_status = self.url_sevice + '/status'
        r = requests.get(url_status)

        if r.status_code == 200:
            logger.info(r.json())
        else:
            logger.error(r.status_code)

    def register_service(self):
        url_register = self.url_sevice + '/client/register'
        command = {'guid':self._machineGuid}

        r = requests.post(url_register,json = command, auth=BodyDigestSignature(self._secret))

        if r.status_code == 200:
            message = r.json()

            if message['ack']:
                logger.info(message['status'])

            else:
                logger.error(message['error'])
        else:
            logger.warning(r.content)

    def get_questions(self):
        url_q = self.url_sevice + '/questions/list'

        r = requests.get(url_q,headers={"x-client-guid":self._machineGuid})

        if r.status_code == 200:

            handler = QuestionHandler(r.json())
            valid_ones = handler.get_valid_questions()

            for valid in valid_ones:
                logger.info(valid)

        else:
            logger.error(r.content)
import time

if __name__== "__main__":
  client = ClientService('config.json')

  client.register_service()
  client.get_questions()