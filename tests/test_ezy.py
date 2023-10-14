#!/usr/bin/python3
"""A test for ezy functions... run test in root dir
"""

from models.ezy import Ezy
from models import storage_type

ins = Ezy()
ins.original_url = "https://www.14_10_2023_16:47.com"
ins.save()  # save instance
print(ins)  # print saved instance
print("\n\n\t\tTest to_dict()")
ins_json = ins.to_dict()  # expects a json representation of the instance
print(ins_json)


print("\n\n\t Test delete() and retrieve an object based on original url")

inst = Ezy()
inst.original_url = "https://www.yubuno.com/dfsdfios-sfsfskfsdbfs"
inst.save()

print("\n\tGET")
print(storage_type.all(inst.original_url))  # retrieves the instance

print("\n\tDelete")
inst.remove_url()  # delete the instance
print("\n\tREMOVED SUCCESSFULLY")

print("\n\tCheck if instance still exists")
print(storage_type.all(inst.original_url))

print('\n\tretrieve an object based on short url')
third_ins = Ezy()
third_ins.original_url = "https://www.yandex.com-blog-about-us"
third_ins.save()

print(storage_type.all(None, third_ins.short_url))

print('\n\tTest count() to retrieve the number of records in the database')

print(storage_type.count())
