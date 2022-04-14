import json


class ConfigHandler(object):
    def __init__(self, pathToConfigFile):
        """sets config file path (full)"""
        self.path = pathToConfigFile

    def read_config_file(self):
        """reads the configuration file, defined in constructor, with the json package"""
        with open(self.path, "r") as json_file:
            self.data = json.load(json_file)
        return self.data
