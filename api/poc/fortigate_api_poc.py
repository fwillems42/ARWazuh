import sys
from time import sleep

from api.fortigate_api import FortiGateApi, FortiGateObject
from domain import utils


def fprint(content, inline=False, use_stdout=True):
    output = content if inline else content + "\n"

    if use_stdout:
        sys.stdout.write(output)
    else:
        with open('exec.log', 'a') as f:
            f.write(output)


def main():
    api = FortiGateApi("192.168.3.158")
    debug = True

    isolation_group_name = 'Isolation'
    mac_object_name = 'Victim'
    mac_object = FortiGateObject.create_mac_object(mac_object_name, '00:0C:29:AF:40:81')

    fprint(f"[1] get_all_addr_object_response: ", inline=True)
    get_all_addr_object_response = api.get_all_addr_object()
    if debug:
        fprint(utils.pprint_json(get_all_addr_object_response))

    sleep(2.0)

    fprint(f"[2] add_mac_object_response: ", inline=True)
    add_mac_object_response = api.add_mac_object(mac_object)
    if debug:
        fprint(utils.pprint_json(add_mac_object_response))

    sleep(2.0)

    fprint(f"[3] get_all_addr_object_response: ", inline=True)
    get_all_addr_object_response = api.get_all_addr_object()
    if debug:
        fprint(utils.pprint_json(get_all_addr_object_response))

    sleep(2.0)

    fprint(f"[4] get_members_of_group_response: ", inline=True)
    get_members_of_group_response = api.get_members_of_group(isolation_group_name)
    if debug:
        fprint(utils.pprint_json(get_members_of_group_response))

    sleep(2.0)

    fprint(f"[5] add_object_to_group_response: ", inline=True)
    add_object_to_group_response = api.add_object_to_group(mac_object_name, isolation_group_name)
    if debug:
        fprint(utils.pprint_json(add_object_to_group_response))

    sleep(2.0)

    fprint(f"[6] get_members_of_group_response: ", inline=True)
    get_members_of_group_response = api.get_members_of_group(isolation_group_name)
    if debug:
        fprint(utils.pprint_json(get_members_of_group_response))

    sleep(2.0)

    fprint(f"[7] remove_object_from_group_response: ", inline=True)
    remove_object_from_group_response = api.remove_object_from_group(mac_object_name, isolation_group_name)
    if debug:
        fprint(utils.pprint_json(remove_object_from_group_response))

    sleep(2.0)

    fprint(f"[8] get_members_of_group_response: ", inline=True)
    get_members_of_group_response = api.get_members_of_group(isolation_group_name)
    if debug:
        fprint(utils.pprint_json(get_members_of_group_response))

    sleep(2.0)

    fprint(f"[9] remove_mac_object_response: ", inline=True)
    remove_mac_object_response = api.remove_mac_object(mac_object_name)
    if debug:
        fprint(utils.pprint_json(remove_mac_object_response))

    sleep(2.0)


if __name__ == '__main__':
    main()
