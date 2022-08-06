#!/usr/bin/python3
"""
File Storage Module
"""
import json
from json import JSONEncoder
from json import JSONDecoder
from datetime import datetime
from os.path import exists


class DateTimeEncoder(JSONEncoder):
    """ DateTimeEncoder to encode datetime objects to json"""

    def default(self, o):
        """ Default encoding """
        if isinstance(o, (datetime, datetime.date)):
            return o.isoformat()
        return super().default(o)


class DateTimeDecoder(JSONDecoder):
    """ Custom DateTimeDecoder """

    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        super().__init__(**kwargs)

    def object_hook(self, dict_):
        """Try to decode a complex number."""
        dic = {}
        for key, value in dict_.items():
            try:
                dic[key] = datetime.fromisoformat(value)
            except (ValueError, TypeError, json.decoder.JSONDecodeError):
                dic[key] = value
        return dic


class FileStorage:
    """ File Storage Objects Representation """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects """
        return FileStorage.__objects

    def new(self, obj):
        """ add new object to dictionary of objects"""
        FileStorage.__objects[
            f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """ save objects dictionary to json file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(FileStorage.__objects, cls=DateTimeEncoder))

    def reload(self):
        """ Desirialize, load object from json"""
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                result = file.read()
                if result:
                    FileStorage.__objects = json.loads(
                        result, cls=DateTimeDecoder)
                else:
                    FileStorage.__objects = {}
