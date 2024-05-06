from api.pfsense_api import PfSenseApi, PfSenseRule
from domain import utils


def main():
    api = PfSenseApi("10.10.15.1")
    debug = False

    print(f"Getting all rules..", end=" ")
    get_all_rules_response = api.get_firewall_rules()
    print(f"{get_all_rules_response['message']}")
    if debug:
        print(utils.pprint_json(get_all_rules_response))

    custom_rule = PfSenseRule.create_default_rule()

    print(f"Posting custom rule..", end=" ")
    post_custom_rule_response = api.post_firewall_rule(custom_rule)
    custom_rule_tracker = post_custom_rule_response['data']['tracker']
    print(post_custom_rule_response['message'])

    if debug:
        print(f"Tracker: {custom_rule_tracker}")
        print(utils.pprint_json(post_custom_rule_response))

    input("Press any button to continue..")

    print(f"Deleting custom_rule..", end=" ")
    delete_custom_rule_response = api.delete_firewall_rule(custom_rule_tracker)
    print(delete_custom_rule_response['message'])

    if debug:
        print(utils.pprint_json(delete_custom_rule_response))

    print("Committing configuration..", end=" ")
    apply_configuration_response = api.apply(asynchronous=False)
    print(apply_configuration_response['message'])

    if debug:
        print(utils.pprint_json(apply_configuration_response))


if __name__ == '__main__':
    main()
