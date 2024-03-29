import json


def filter_dictionary(dictionary, filters):
    return [entry for entry in dictionary if all(entry.get(key) == value for key, value in filters.items())]


def pprint_json(data: any):
    print(json.dumps(data, indent=4, sort_keys=True))
