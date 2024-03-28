#!/usr/bin/python3
# Copyright (C) 2015-2022, Wazuh Inc.
# All rights reserved.

# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

import os
import sys
import json
import datetime
from pathlib import PureWindowsPath, PurePosixPath

from api.pfsense_api import PfSenseApi, PfSenseRule
from domain.validator import Validator

if os.name == 'nt':
    LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"
else:
    LOG_FILE = "/var/ossec/logs/active-responses.log"

ADD_COMMAND = 0
DELETE_COMMAND = 1
CONTINUE_COMMAND = 2
ABORT_COMMAND = 3

OS_SUCCESS = 0
OS_INVALID = -1


class Message:
    def __init__(self):
        self.alert = None
        self.command = 0


def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(
            str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name_posix + ": " + msg + "\n")


def setup_and_check_message(argv):
    message = Message()

    # get alert from stdin
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break

    write_debug_file(argv[0], input_str)

    try:
        data = json.loads(input_str)
    except ValueError:
        write_debug_file(argv[0], 'Decoding JSON has failed, invalid input format')
        message.command = OS_INVALID
        return message

    message.alert = data

    command = data.get("command")

    if command == "add":
        message.command = ADD_COMMAND
    elif command == "delete":
        message.command = DELETE_COMMAND
    else:
        message.command = OS_INVALID
        write_debug_file(argv[0], 'Not valid command: ' + command)

    return message


def send_keys_and_check_message(argv, keys):
    # build and send message with keys
    keys_msg = json.dumps(
        {"version": 1, "origin": {"name": argv[0], "module": "active-response"}, "command": "check_keys",
         "parameters": {"keys": keys}})

    write_debug_file(argv[0], keys_msg)

    print(keys_msg)
    sys.stdout.flush()

    # read the response of previous message
    input_str = ""
    while True:
        line = sys.stdin.readline()
        if line:
            input_str = line
            break

    write_debug_file(argv[0], input_str)

    try:
        data = json.loads(input_str)
    except ValueError:
        write_debug_file(argv[0], 'Decoding JSON has failed, invalid input format')
        return None

    action = data.get("command")

    if "continue" == action:
        ret = CONTINUE_COMMAND
    elif "abort" == action:
        ret = ABORT_COMMAND
    else:
        ret = OS_INVALID
        write_debug_file(argv[0], "Invalid value of 'command'")

    return ret


def extract_data(ar_name, alert):
    try:
        rule_id = alert["rule"]["id"]
        match rule_id:
            case "130000":
                return alert["data"]["src_ip"], alert["id"], rule_id
            case _:
                return None, '-1'
    except Exception as error:
        write_debug_file(ar_name, f"Error while extracting data using {ar_name} AR : {error} ")


def main(argv):
    write_debug_file(argv[0], "Started")

    # validate json and get command
    msg = setup_and_check_message(argv)
    alert = msg.alert["parameters"]["alert"]

    src_ip, alert_id, rule_id = extract_data(argv[0], alert)
    if not Validator.validate_ip(src_ip):
        if src_ip is None:
            write_debug_file(argv[0], json.dumps(msg.alert) + f" {rule_id} Missing implementation in {argv[0]} AR")
        else:
            write_debug_file(argv[0], f"{src_ip} is not a valid ip")
        sys.exit(OS_INVALID)

    if msg.command < 0:
        sys.exit(OS_INVALID)

    if msg.command == ADD_COMMAND:

        """ Start Custom Key
        At this point, it is necessary to select the keys from the alert and add them into the keys array.
        """

        keys = [rule_id]

        """ End Custom Key """

        action = send_keys_and_check_message(argv, keys)

        # if necessary, abort execution
        if action != CONTINUE_COMMAND:

            if action == ABORT_COMMAND:
                write_debug_file(argv[0], "Aborted")
                sys.exit(OS_SUCCESS)
            else:
                write_debug_file(argv[0], "Invalid command")
                sys.exit(OS_INVALID)

        """ Start Custom Action Add """
        try:
            '''
                TODO: We use the API of pfSense to ban the src_ip address we got from the alert
                We might need alternative services like NAC, Asset Manager, AI, to gather additional information about the 
                machine we target such as VLan, Gateway, DNS...
                
                We get the ip of the device that manages the target, we also need to know what type of device we need to talk with
                Only then we can use the correct module to handle the alert
                If it's a switch, we need to down the port or put it in a blackhole vlan
                If it's a firewall, we might want to add a specific rule to block all incoming traffic from the src_ip
                And so on..
                
                In this example, we will stick with a static ip to moq the action of getting the management_ip
                we also only target pfsense firewall, we need to handle the deletion of the rule in case of a stateful AR
                to simplify the search and deletion/deactivation of the rule we will use the event_id in the description of the FW rule
                
                In this case we might also want to know on which interface we want to block the traffic, 
                we just need to ask the firewall to give us all the interface and choose the one that fits in with the src_ip
            '''
            management_ip = "10.10.15.1"
            api = PfSenseApi(management_ip)
            custom_rule = PfSenseRule.create_custom_rule(
                {
                    'interface': 'em2',
                    'src': src_ip,
                    'descr': f'AR: Blocking all incoming traffic from {src_ip} ({alert_id})'
                }
            )
            api.post_firewall_rule(custom_rule)
            api.apply()

            write_debug_file(argv[0],
                             json.dumps(msg.alert) + f" {rule_id} Successfully banning threat using {argv[0]} AR")
        except OSError as error:
            write_debug_file(argv[0],
                             json.dumps(msg.alert) + f" {rule_id} Error banning threat using {argv[0]} AR : {error}")

        """ End Custom Action Add """

    elif msg.command == DELETE_COMMAND:

        """ Start Custom Action Delete """
        try:
            management_ip = "10.10.15.1"
            api = PfSenseApi(management_ip)

            # We need the tracker id of the rule we added
            fw_rule = api.get_specific_firewall_rules(
                {
                    'descr': f'AR: Blocking all incoming traffic from {src_ip} ({alert_id})'
                }
            )

            api.delete_firewall_rule(fw_rule['tracker'])
            write_debug_file(argv[0],
                             json.dumps(msg.alert) + f" {rule_id} Successfully unbanning threat using {argv[0]} AR")
        except OSError as error:
            write_debug_file(argv[0],
                             json.dumps(msg.alert) + f" {rule_id} Error unbanning threat using {argv[0]} AR : {error}")

        """ End Custom Action Delete """

    else:
        write_debug_file(argv[0], "Invalid command")

    write_debug_file(argv[0], "Ended")

    sys.exit(OS_SUCCESS)


if __name__ == "__main__":
    main(sys.argv)
