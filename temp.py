import json
from cs50 import SQL
from flask import 

db = SQL('sqlite:///butterfly-effect.db')

json_object = {}



object = {
    'id': 1,
    'message': 'hello',
    'children': [{
        'id': 2,
        'message': 'hello',
        'children': [{
            'id': 4,
            'message': 'hello',
            'children': []
        }]
    },
    {
        'id': 3,
        'message': 'bye',
        'children': []
    }]
    }

with open('file.json', 'w') as f:
    json.dump(object, f, indent=2)
    print("The json file is created")

