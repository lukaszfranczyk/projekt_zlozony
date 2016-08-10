import yaml
from .metaclasses import Singleton


class Config(dict, metaclass=Singleton):

    def __init__(self):
        with open('conf/settings.yaml') as conf_file:
            self.update(yaml.load(conf_file))
