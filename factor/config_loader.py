import os
import json

__config_item__ = {}


def get_config_item(config_file_name, item_name, config_file_extension=".json"):
    try:
        config_item = __config_item__[(config_file_name, item_name)]
    except KeyError:
        abs_path = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(abs_path, "config", config_file_name)+config_file_extension
        with open(config_file_path) as config_file:
            config_item = json.load(config_file)[item_name]
    return config_item
