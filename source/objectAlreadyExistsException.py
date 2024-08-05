#!/bin/python3

class ObjectAlreadyExistsException(Exception):
    """This exception is raised when the dataHandler should create an entry or a category that already exists with the same name"""
    pass
