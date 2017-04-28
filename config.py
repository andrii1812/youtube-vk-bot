import json


class Config:
    config = None

    @classmethod
    def get_config(self):
        if not self.config:
            self.config = json.load(open('config.json', 'r'))
        return self.config