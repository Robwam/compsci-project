import Scheduler.Configuration.config as config
from pony.orm import *

DB = Database()
DB.bind(provider='sqlite', filename=config.database_file)

def setup():
    DB.generate_mapping(create_tables=True)
