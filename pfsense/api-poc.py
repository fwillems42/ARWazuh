import json
import os

import requests
import urllib3

# Temporarily disabling InsecureRequestWarning due to self-signed certificate
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class API:
    """
        Basic implementation of some of the endpoints provided by the following pfsense-api:
            https://github.com/jaredhendrickson13/pfsense-api

    """

    def __init__(self, domain: str):
        self.schema = f"https://{domain}"

        # Create .env file with the following keys/values
        # API_USER="xxx"
        # API_PASS="xxx"

        load_dotenv()
        __user = os.getenv('API_USER')
        __pass = os.getenv('API_PASS')

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


def pprint(data: any):
    print(json.dumps(data, indent=4, sort_keys=True))


def create_custom_rule():
    return {
        "type": "pass",
        "interface": "lan",
        "ipprotocol": "inet",
        "protocol": "tcp/udp",
        "src": "10.10.15.55",
        "srcport": "any",
        "dst": "any",
        "dstport": "any",
        "descr": "Block traffic from 10.10.15.55",
        "top": True,
        "apply": True
    }


def main():
    api = API("10.10.15.1")
    debug = False

    print(f"Getting all rules..", end=" ")
    get_all_rules_response = api.get_firewall_rules()
    print(f"{get_all_rules_response['message']}")
    if debug:
        pprint(get_all_rules_response)

    custom_rule = create_custom_rule()

    print(f"Posting custom rule..", end=" ")
    post_custom_rule_response = api.post_firewall_rule(custom_rule)
    custom_rule_tracker = post_custom_rule_response['data']['tracker']
    print(post_custom_rule_response['message'])

    if debug:
        print(f"Tracker: {custom_rule_tracker}")
        pprint(post_custom_rule_response)

    input("Press any button to continue..")

    print(f"Deleting custom_rule..", end=" ")
    delete_custom_rule_response = api.delete_firewall_rule(custom_rule_tracker)
    print(delete_custom_rule_response['message'])

    if debug:
        pprint(delete_custom_rule_response)

    print("Committing configuration..", end=" ")
    apply_configuration_response = api.apply(asynchronous=False)
    print(apply_configuration_response['message'])

    if debug:
        pprint(apply_configuration_response)


if __name__ == '__main__':
    main()
