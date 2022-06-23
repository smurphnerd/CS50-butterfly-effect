from cs50 import SQL

db = db = SQL('sqlite:///butterfly-effect.db')

parent = db.execute('SELECT * FROM nodes WHERE user_id = ? AND key = ?', '1', '1')
if not parent:
    print('nothing')
    
    # Get key for child
else:
    key = parent[0]['key'] + '.' + str(db.execute('SELECT COUNT(key) FROM children WHERE user_id = ? AND key = ?', '1', '1')[0]['COUNT(key)'] + 1)
    print(key)