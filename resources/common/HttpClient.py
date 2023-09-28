"""Copyright (c) 2021 ULAK Communications
This file contains basic http operations for GET, POST, DELETE methods
"""

import requests
from common.Logger import log

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpClient:

    def __init__(self, ip, port, user=None, password=None, api_path=None, protocol='http'):
        self.user = user
        self.password = password
        self.url = f'{protocol}://{ip}:{port}/{api_path}'
        log.info(f"url ---> {self.url} username ---> {user} password ---> {password}")

    def get(self, path=None):

        try:
            updated_url = self.url + path if path else self.url
            response = requests.get(updated_url, auth=(self.user, self.password), verify=False)
            log.info("get response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            log.error(f"get response error---> {e}")

    def post(self, path=None, data=None, files=None):

        try:
            updated_url = self.url + path if path else self.url
            response = requests.post(updated_url, auth=(self.user, self.password), json=data, files=files, verify=False)
            log.info("post response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            log.error(f"post response error---> {e}")

    def delete(self, path=None):
        try:
            updated_url = self.url + path if path else self.url
            response = requests.delete(updated_url, auth=(self.user, self.password))
            log.info("delete response received successfully")
            return response
        except requests.exceptions.RequestException as e:
            log.error(f"delete response error---> {e}")
