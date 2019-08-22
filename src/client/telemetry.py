import os
import sys
from dateutil import parser
from datetime import date, timedelta, datetime
import browserhistory as bh
import pytz
import psutil
import pytz
from datetime import datetime, timezone
#from tzlocal import get_localzone
import tldextract
from tzlocal import get_localzone

class Telemetry():

    OBS_TYPES = (
        ('U', 'URL'),
        ('I', 'IP'),
        ('D', 'DomainName'),
        ('F', 'FileHash'),
        ('P', 'ProcessName'),
        ('R', 'RegistryKey'),
    )

    def __init__(self):
        self.local_zone = get_localzone()
        local_tz = pytz.timezone(self.local_zone.zone)

        self.now_tz = local_tz.localize(datetime.utcnow(), is_dst=None)

        self.bh_history = None

    def search_domain(self,text):

        self.bh_history = bh.get_browserhistory()

        count = 0
        for browser in self.bh_history.keys():
            history = self.bh_history[browser]

            for entry in history:
                (url,title,datetime) = entry
                ext = tldextract.extract(url)
                #join domain and tld
                if ext.registered_domain == text: count+=1
        return count

    def search_IP(self,text):

        connections = psutil.net_connections()
        count = 0
        for connection in connections:
            if connection.raddr:
                if connection.raddr.ip == text:
                    count += 1
        return count

    def search_url(self,text):
        self.bh_history = bh.get_browserhistory()

        count = 0
        for browser in self.bh_history.keys():
            history = self.bh_history[browser]

            for entry in history:
                (url,title,datetime) = entry
                if url == text: count +=1
        return count

    def handle_observable(self,question):

        if question['completed'] == False:

            begin_dt = parser.parse(question['begin_datetime'])
            end_dt = parser.parse(question['end_datetime'])

            if self.now_tz > end_dt or self.now_tz < begin_dt:
                status = 'Question is expired'
                return (status, 0)

            #this is a domain request
            if question['observable_type'] in ['U','I','D','F','F','P','R']:
                status = 'OK'
                if question['observable_type'] == 'D':
                    count = self.search_domain(question['observable'])
                    return (status,count)
                elif question['observable_type'] == 'U':
                    count = self.search_url(question['observable'])
                    return (status, count)
                elif question['observable_type'] =='I':
                    count = self.search_IP(question['observable'])
                    return (status, count)
            else:
                status='Observable not supported'
                return (status,0)

        else:
            status = 'Question is closed'
            return (status, 0)