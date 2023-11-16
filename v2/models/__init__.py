#!/usr/bin/python3

from models.engine.db_storage import DBStorage
# Creates an instance of the database model and connects to
# database module using the storage_type variable


storage_type = DBStorage()
storage_type.reload()
