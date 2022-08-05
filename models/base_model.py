from re import U
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """This is the base model from which all models will come from"""

    id = str(uuid4())
    created_at = datetime.now()
    updated_at = datetime.now()

    def __str__(self):
        """prints the class name, id and the __dict of the instance"""
        return (f"{__class__.__name__} {self.id} {self.__dict__}")
    

    def save(self):
        """updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.datetime.now()
    
    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__ of the instance"""
        updated_dict = dict(self.__dict__)
        updated_dict["__class__"] = self.__class__.__name__
        updated_dict["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        updated_dict["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return updated_dict
        
    