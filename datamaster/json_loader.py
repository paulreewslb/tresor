import os
import json

__json_data__ = {}


def get_json_data(json_file_folder, json_file_name):
    try:
        json_data = __json_data__[(json_file_folder, json_file_name)]
    except KeyError:
        abs_path = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(abs_path, json_file_folder, json_file_name)+".json"
        with open(json_file_path) as json_file:
            json_data = json.load(json_file)
    return json_data
