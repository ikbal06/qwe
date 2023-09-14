"""Copyright (c) 2021 ULAK Communications
This file contains basic http operations for GET,POST,DELETE methods
"""

import requests
from common.Logger import log

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpClient:

    def __init__(self, ip,port ,user=None, password=None,api_path=None, protocol='http'):
        self.user = user
        self.password = password
        self.url = '{}://{}:{}/{}'.format(protocol, ip,port, api_path)
        print("url ---> {} username ---> {} password ---> {}  ".format(self.url, self.user, self.password))

    def get(self, path=None):

        try:
            if path:
              updated_url = self.url + path
            else:
              updated_url = self.url
            response = requests.get(updated_url, auth=(self.user, self.password), verify=False)
            print("get response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            print("get response error---> {}".format(e))

    def post(self, path=None, data=None,files=None):

        try:
            if path:
              updated_url = self.url + path
            else:
              updated_url = self.url
            response = requests.post(updated_url,auth=(self.user, self.password), json=data,files=files, verify=False)
            print("post response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            print("post response error---> {}".format(e))

    def delete(self, path=None):
        try:
            if path:
              updated_url = self.url + path
            else:
              updated_url = self.url         
            response = requests.delete(updated_url, auth=(self.user, self.password))
            print("delete response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            print("delete response error---> {}".format(e))
