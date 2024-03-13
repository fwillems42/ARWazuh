import os

import requests
import urllib3
# Temporarily disabling InsecureRequestWarning due to self-signed certificate
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PfSenseRule:

    @staticmethod
    def create_default_rule():
        return {
            "type": "pass",
            "interface": "lan",
            "ipprotocol": "inet46",
            "protocol": "tcp/udp",
            "src": "any",
            "srcport": "any",
            "dst": "any",
            "dstport": "any",
            "descr": "Pattern rule",
            "top": True,
            "apply": True
        }

    @staticmethod
    def create_custom_rule(rule):
        # Get default rule
        pattern = PfSenseRule.create_default_rule()

        # Apply custom values
        for key, value in rule.items():
            pattern[key] = value

        return pattern


class PfSenseApi:
    """
        Basic implementation of some of the endpoints provided by the following pfsense-api:
            https://github.com/jaredhendrickson13/pfsense-api

    """

    def __init__(self, domain: str):
        self.schema = f"https://{domain}"

        # Create .env file with the following keys/values
        # XXX_API_USER="xxx"
        # XXX_API_PASS="xxx"

        load_dotenv()
        __user = os.getenv('PFSENSE_API_USER')
        __pass = os.getenv('PFSENSE_API_PASS')

        self.session = requests.Session()
        self.session.auth = (__user, __pass)

    def get_firewall_rules(self):
        full_url = f"{self.schema}/api/v1/firewall/rule"
        response = self.session.get(full_url, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['code']}

    def post_firewall_rule(self, rule: any):
        full_url = f"{self.schema}/api/v1/firewall/rule"
        response = self.session.post(full_url, json=rule, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['code']}

    def delete_firewall_rule(self, tracker: str):
        full_url = f"{self.schema}/api/v1/firewall/rule?tracker={tracker}"
        response = self.session.delete(full_url)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['code']}

    def apply(self, asynchronous: bool = True):
        full_url = f"{self.schema}/api/v1/firewall/apply"
        response = self.session.post(full_url, {'async': asynchronous}, verify=False)
        response_json = response.json()

        if response.status_code == 200:
            return response_json
        else:
            return {'error_code': response_json['code']}

