import json

config = {}

with open('./mysqldb/config.json') as f:
    config = json.load(f)