import os
import string
import random
from yaml import load, dump

class Utils(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_salt(length):
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(length))


class Config(object):
    def __init__(self, filename='config.yml'):
        self.filename = filename
        self.config = None

    def load_config(self):
        with open(self.filename, 'r') as conf:
            self.conf = load(conf)

    def get(self, default, key=None):
        if key is None:
            return None
        elif self.config is None:
            return default
        else:
            return self.config[key]

    def set(self, key, value):
        """
        This allows for the saving of custom fields
        """
        dump({key: value}, self.filename)
