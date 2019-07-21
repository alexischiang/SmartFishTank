import sqlite3 as sql

path = 'database/'
users = sql.connect(path + 'users.db')
statics = sql.connect(path + 'statics.db')
udb = users.cursor()
sdb = statics.cursor()


members = sdb.execute('''
    Select * From membership
''')
for row in members:
    print(row[0])