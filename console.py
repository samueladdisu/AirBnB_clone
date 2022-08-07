#!/usr/bin/python3
"""
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb) help quit
Quit command to exit the program
"""
import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """command line"""
    prompt = "(hbnb)"

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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
