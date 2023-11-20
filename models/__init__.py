#!/usr/bin/python3
""" instantiate an object """

from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()
