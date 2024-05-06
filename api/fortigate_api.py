import os

import requests
import urllib3
from dotenv import load_dotenv

# Temporarily disabling InsecureRequestWarning due to self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FortiGateObject:

    @staticmethod
    def create_mac_object(name, mac):
        return {
            "name": name,
            "type": "mac",
            "macaddr": [{"macaddr": mac}],
            "color": "0"
        }


class CustomSessionApi(requests.Session):

    def __init__(self, api_key):
        super().__init__()
        self.__key = api_key

    def prepare_request(self, request):
        request = super().prepare_request(request)
        request.url += ('&' if '?' in request.url else '?') + f'access_token={self.__key}'
        return request


class FortiGateApi:
    """
        Basic implementation of some endpoints provided by the fortigate api

    """

    def __init__(self, domain: str):
        self.schema = f"https://{domain}"

        # Create .env file with the following keys/values
        # XXX_API_USER="xxx"
        # XXX_API_PASS="xxx"

        load_dotenv()
        __key = os.getenv('FORTIGATE_API_KEY')

        self.session = CustomSessionApi(__key)

    def get_all_addr_object(self):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/address"
        response = self.session.get(full_url, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}

    def get_members_of_group(self, group_name):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/addrgrp/{group_name}/member"
        response = self.session.get(full_url, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}

    def add_mac_object(self, mac: dict):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/address"
        response = self.session.post(full_url, json=mac, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}

    def remove_mac_object(self, object_name: str):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/address"
        response = self.session.delete(full_url, json={"name": object_name}, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}

    def add_object_to_group(self, object_name, group_name):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/addrgrp/{group_name}/member"
        response = self.session.post(full_url, json={"name": object_name}, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}

    def remove_object_from_group(self, object_name, group_name):
        full_url = f"{self.schema}/api/v2/cmdb/firewall/addrgrp/{group_name}/member/{object_name}"
        response = self.session.delete(full_url, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['http_status']}
