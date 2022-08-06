#!/usr/bin/python3
"""
This is the base model documentation
"""
from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    """This is the base model from which all models will come from"""

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at, updated_at"]:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """prints the class name, id and the __dict of the instance"""
        return (f"{__class__.__name__} {self.id} {self.__dict__}")

    def save(self):
        """
        updates the public instance attribute updated_at
        """
        setattr(self, "updated_at",  datetime.now())
        storage.save()

    def to_dict(self):
        dic = {}
        for key, value in self.__dict__.items():
            if key in ["updated_at", "created_at"]:
                dic[key] = value.isoformat()
            else:
                dic[key] = value
        dic["__class__"] = self.__class__.__name__
        return dic
