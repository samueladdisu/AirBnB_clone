#!/usr/bin/python3
"""
The main console
"""
import cmd, sys


class HBNBCommand(cmd.Cmd):
    """command line"""
    def do_quit(self, arg):
        """write quit to exit"""
        try:
            sys.exit(int(arg))
        except(ValueError, TypeError):
            sys.exit(0)
