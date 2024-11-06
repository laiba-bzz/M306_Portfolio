from dataclasses import dataclass
from datetime import date


class GreenItem:
    def __init__(self, item_id, title, description):
        self.item_id = item_id
        self.title = title
        self.description = description

    def get_description(self):
        return {'description': self.description}

