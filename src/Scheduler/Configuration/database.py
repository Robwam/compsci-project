import Scheduler.Configuration.config as config
from pony.orm import *

DB = Database()

def setup(filename=None):

    if filename is None:
        filename = config.database_file

    # Create the file if doesn't already exist
    open(filename, 'w+').close()

    DB.bind(provider='sqlite', filename=filename)
    DB.generate_mapping(create_tables=True)
