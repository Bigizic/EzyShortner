#!/usr/bin/python3
"""A class that sets the parameters needed and add other funtionality
basically the entry point
"""


import datetime
import uuid
from shortner.url_shortner import url_shortner


class Ezy():
    """default storage: MySql db"""
    __file_path = "ezy.json"

    def __init__(self, original_url):
        """Sets the default parameters"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.utcnow()
        self.original_url = original_url
        self.short_url = url_shortner(original_url)

    def to_dict(self):
        """Creates a dictionary representation of the instance
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "original_url": self.original_url,
            "short_url": self.short_url
        }

    def save(self):
        """Writes information about the `Ezy` instance to a JSON file
        """
        with open(self.__file_path, "w") as open_file:
            open_file.write(str(self.to_dict()) + "\n")


def create_ezy_instance(original_url):
    return Ezy(original_url)
