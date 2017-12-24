import Scheduler.Configuration.config as config
from pony.orm import *

import os

DB = Database()

'''
Opens/creates an sqlite database and maps objects

Args:
    Str filename: The filename of the database, defaults to the one set in config
'''
def setup(filename=None):

    if filename is None:
        filename = config.database_file

    path = os.path.join(os.getcwd(), filename)

    # Create the file if doesn't already exist
    open(path, 'a').close()

    DB.bind(provider='sqlite', filename=path)
    DB.generate_mapping(create_tables=True)

'''
Deletes database

Args:
    Str filename: The filename of the database, defaults to the one set in config
'''
def teardown(filename=None):
    if filename is None:
        filename = config.database_file

    path = os.path.join(os.getcwd(), filename)

    os.remove(path)
