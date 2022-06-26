import json
from cs50 import SQL

db = SQL('sqlite:///butterfly-effect.db')

root_object = {}
root_data = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', )[0]
root_object['id'] = root_data['id']
root_object['message'] = root_data['message']
add_children(root_object)

def add_children(root_object):
    children = db.execute('SELECT * FROM children WHERE node_id = ?', )
    if len(children) > 0:
        root_object['children'] = []
        for child in children:
            child_object = {}
            child_data = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', )[0]
            child_object['id'] = child_data['id']
            child_object['message'] = child_data['message']
            add_children(child_object)
            root_object['children'].append(child_object)
            return
    else:
        return

"""
define root attributes

Add children (root)
    If root has children
        root[children] = []
        For each child, add attributes
        Add children (child)
        Append child to root children
    else
        return
"""