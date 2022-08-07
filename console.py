#!/usr/bin/python3
"""
The main console
"""
import cmd
import sys
import json
from models.base_model import BaseModel
import models
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State



class HBNBCommand(cmd.Cmd):
    """command line"""
    intro = "(hbnb) help\n\nDocumented commands (type help <topic>):\n========================================\n\nEOF  help  quit\n\n(hbnb)\n(hbnb) help quit\n\nQuit command to exit the program\n"
    prompt = "(hbnb) "
    __classes = {"BaseModel": BaseModel, "State": State,
                "Place": Place, "Review": Review,
                "Amenity": Amenity, "User": User, "City": City}

    def do_quit(self, arg):
        """write quit to exit"""

        try:
            sys.exit(int(arg))
        except(ValueError, TypeError):
            sys.exit(0)

    def help_quit(self):
        """ help doc """
        print("Enter Quit to Exit program")

    def do_EOF(self, args):
        """ Exit program on CTRL+D"""
        print(args)
        sys.exit(-1)

    def help_EOF(self):
        """ hellp EOF """
        print("Exit Program on CTRL+D")

    def emptyline(self):
        """Overrides the emptyline without"""
        pass

    def do_create(self, args):

        """ Create New Object of BaseModel
            Syntax: create [ModelName]"""
        if not args:
            print("** class name missing **")
        elif args not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_object = HBNBCommand.__classes[args]()
            new_object.save()
            print(new_object.id)

    def help_create(self):

        """ doc create """
        print("Create New Object of BaseModel")
        print("Syntax: Create [ModelName]")

    def do_show(self, args):

        """ Print instance of object of given id
         Syntax: show [ModelName] [id]"""
        if not args:
            print("** class name missing **")
        elif args.split(" ")[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args.split(" ")) == 1:
            print("** instance id missing **")
        else:
            models.storage.reload()
            objects = models.storage.all()
            class_name = args.split(" ")[0]
            _id = args.split(" ")[-1]
            obj = objects.get(f"{class_name}.{_id}", "** no instance found **")
            print(obj)

    def help_show(self):

        """ doc """
        print("Print Instance of Object of given Id")
        print("Syntax: show [ModelName] [Id]")

    def do_destroy(self, args):

        """ Destroy an object \n Syntax: destroy [ModelName] [id]"""
        if not args:
            print("** class name missing **")
        elif args.split(" ")[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args.split(" ")) == 1:
            print("** instance id missing **")
        else:
            models.storage.reload()
            objects = models.storage.all()
            class_name = args.split(" ")[0]
            _id = args.split(" ")[-1]
            obj = objects.get(f"{class_name}.{_id}", None)
            if obj:
                del objects[f"{class_name}.{_id}"]
            else:
                print("** no instance found **")
            models.storage.save()

    def help_destroy(self):

        """ doc """
        print("Destroy an object")
        print("Syntax: destroy [ModelName] [id]")

    def do_all(self, args):

        """ Print all objects
            Syntax: all [ModelName] (optional)"""
        if args and args in HBNBCommand.__classes:
            models.storage.reload()
            objects = models.storage.all()
            for key, value in objects.items():
                if key.split(".")[0] == args:
                    print(value)
        elif not args:
            models.storage.reload()
            objects = models.storage.all()
            for value in objects.values():
                print(value)
        else:
            print("** class doesn't exist **")

    def help_all(self):

        """ doc """
        print("Print all objects")
        print("Syntax: all [ModelName] (optional)")

    def do_update(self, args):

        """ update /add attribute
            Syntax: update [ModelName] [id] [attribute] [value]"""
        if not args:
            print("** class name missing **")
        elif args.split(" ")[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            data = []
            for item in args.split(" ")[1:]:
                if item:
                    data.append(item)
            if len(data) == 0:
                print("** instance id missing **")
            else:
                models.storage.reload()
                objects = models.storage.all()
                key = f"{args.split(' ')[0]}.{data[0]}"
                obj = objects.get(key, None)
                if not obj:
                    print("** no instance found **")
                elif obj and len(data) == 1:
                    print("** attribute name missing **")
                elif obj and len(data) == 2:
                    print("** value missing **")
                else:
                    new_object = (obj.to_dict()).copy()
                    del new_object["__class__"]
                    new_object[data[1]] = data[2]
                    del objects[key]
                    newobj = HBNBCommand.__classes[
                        args.split(" ")[0]](**new_object)
                    newobj.save()

    def help_update(self):

        """ doc """
        print("Update or attribute")
        print("Syntax: update [ModelName] [id] [attribute] [value]")

    def default(self, line):

        """ Default action when command not Known"""
        if len(line.split(".")) > 1 and line.split(".")[1] == "all()":
            obj_list = []
            if line.split(".")[0] == "":
                print("** class name missing **")
            elif line.split(".")[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                models.storage.reload()
                for key, value in models.storage.all().items():
                    if key.split(".")[0] == line.split(".")[0]:
                        obj_list.append(str(value))
                print(obj_list)
        elif len(line.split(".")) > 1 and line.split(".")[1] == "count()":
            count = 0
            if line.split(".")[0] == "":
                print("** class name missing **")
            elif line.split(".")[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                for key in models.storage.all():
                    if key.split(".")[0] == line.split(".")[0]:
                        count += 1
                print(count)
        elif len(line.split(".")) > 1 and line.split(
                ".")[1].split("(")[0] == "show":

            if line.split(".")[0] == "":
                print("** class name missing **")
            elif line.split(".")[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                _id = line.split("(")[1].strip().split(")")[0].strip()[1:-1]
                if _id:
                    self.do_show(f"{line.split('.')[0]} {_id}")
                else:
                    print("** instance id missing **")
        elif len(line.split('.')) > 1 and line.split(
                ".")[1].split("(")[0] == "destroy":
            if line.split(".")[0] == "":
                print("** class name missing **")
            elif line.split(".")[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                _id = line.split("(")[1].strip().split(")")[0].strip()[1:-1]
                if _id:
                    self.do_destroy(f"{line.split('.')[0]} {_id}")
                else:
                    self.do_destroy(f"{line.split('.')[0]}")
        elif len(line.split(".")) > 1 and line.split(
                ".")[1].split("(")[0] == "update":
            if line.split(".")[0] == "":
                print("** class name missing **")
            elif line.split(".")[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                _id = None
                _attr = None
                _val = None
                ok = True
                try:
                    _id = line.split("(")[1].strip().split(
                        ")")[0].strip().split(",")[0].strip()
                    if len(_id) == 0:
                        ok = False
                        print("** instance id missing **")
                    else:
                        models.storage.reload()
                        models.storage.reload()
                        objects = models.storage.all()
                        key = f"{line.split('.')[0]}.{_id[1:-1]}"
                        obj = objects.get(key, None)
                        if not obj:
                            print("** no instance found **")
                            ok = False
                except IndexError:
                    print("** instance id missing **")
                    ok = False
                if ok:
                    d = None
                    try:
                        d = json.loads(",".join(
                            line.split("(")[1].strip().split(
                                ")")[0].strip().split(",")[1:]))
                        for kk, vv in d.items():
                            if kk[0] in ["'", '"']:
                                kk = kk[1:]
                            if vv[0] in ["'", '"']:
                                vv = vv[1:]
                            if kk[-1] in ["'", '"']:
                                kk = kk[:-1]
                            if vv[-1] in ["'", '"']:
                                vv = vv[:-1]
                            self.do_update(
                                f"{line.split('.')[0]} {_id[1:-1]} {kk} {vv}")
                    except Exception:
                        ok = True
                    else:
                        ok = False
                if ok:
                    try:
                        _attr = line.split("(")[1].strip().split(
                            ")")[0].strip().split(",")[1].strip()
                        if _attr[0] in ["'", '"']:
                            _attr = _attr[1:].strip()
                        if _attr[-1] in ["'", '"']:
                            _attr = _attr[:-1].strip()
                    except IndexError:
                        print("** attribute name missing **")
                        ok = False
                if ok:
                    try:
                        _val = line.split("(")[1].strip().split(
                            ")")[0].strip().split(",")[2].strip()
                        if _val[0] in ['"', "'"]:
                            _val = _val[1:].strip()
                        if _val[-1] in ["'", '"']:
                            _val = _val[:-1].strip()
                    except IndexError:
                        print("** value missing **")
                        ok = False
                if ok:
                    self.do_update(
                        f"{line.split('.')[0]} {_id[1:-1]} {_attr} {_val}")
        else:
            super().default(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
