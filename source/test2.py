import logging
import time

import requests
import asyncio
import json
import xml.etree.ElementTree as ET


TOKEN = '8087760670:AAFn0pzO8LsttESIZ73W_Aa26TjZGQmq088'
BOT_USERNAME = '@telePlusStreamCheckBot'

logger = logging.getLogger()
logging.basicConfig(
    filename = '../logs/log.txt',
    encoding = 'utf-8',
    level = logging.INFO
    )

class StreamPlus(object):
    
    def __init__(self):
        self.api_url = self.set_api_url('plus') # plus1 is exmaple
        self.api_header = {"Authorization": "Basic cm9vdDo3ODBAYW1yMTIz"}

    def parse_xml(self, response):
        xml_node = '<>'

    def request_api(self):
        return requests.get(self.api_url, headers = self.api_header)

    def set_api_url(self, plus_indicator):
        plus_nums = {
            'plus': '',
            'plus2': '2',
            'plus3': '3'
        }
        requested_num = plus_nums[plus_indicator] # requested_num will be 1 or 2 or 3 according to plus_indicator
        self.api_url = f'http://185.236.36.132:8087/v2/servers/Wowza%20Streaming%20Engine/vhosts/_defaultVHost_/applications/plus/instances/_definst_/incomingstreams/plus.stream/monitoring/current' 
    
    def extract_info_from_xml_response(self, response):
        pass



 
plus = StreamPlus()
plus.set_api_url('plus') # query.data is one of [plus1, plus2, plus3]
response = plus.request_api()
print(response.text)
# stream_info = plus.extract_info_from_xml_response(response)
