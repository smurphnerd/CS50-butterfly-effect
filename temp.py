import json
from cs50 import SQL
import json


db = SQL('sqlite:///butterfly-effect.db')

def temp(node_id):
    if len(db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', 1, node_id)) != 1:
        return

    thing = 4

    return

temp(60)