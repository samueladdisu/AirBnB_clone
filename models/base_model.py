#!/usr/bin/python3
"""
Base Model to be inherited
"""
import uuid
from datetime import datetime
import models


class BaseModel:

    """ Base Model Representation """
    def __init__(self, *args, **kwargs):

        """ Initialization with or with out kwargs
        kwargs assumed to contain isoformatted datetime object
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["updated_at", "created_at"]:
                        self.__dict__[key] = datetime.fromisoformat(value)
                    else:
                        self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):

        """ String Representation """
        return "[{}] ({}) ({})".format(self.__class__.__name__,
                                       getattr(self, "id"), self.__dict__)

    def save(self):

        """ save instance to file"""
        setattr(self, "updated_at",  datetime.now())
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):

        """ Return Dict Representation """
        dic = self.__dict__.copy()
        dic["updated_at"] = dic["updated_at"].isoformat()
        dic["created_at"] = dic["created_at"].isoformat()
        dic["__class__"] = self.__class__.__name__
        return dic
