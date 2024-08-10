#!/bin/python3
"""
File: datahandler.py
Desc: Exception for already created objects that should be created
"""


class ObjectAlreadyExistsException(Exception):
    """This exception is raised when the dataHandler should create an entry or a category that already exists with the same name"""
