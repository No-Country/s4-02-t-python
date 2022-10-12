from application.db.db import dbConnection

db = dbConnection()

with open('medicamentos.txt', 'r', encoding='utf-8') as m:
    names = list(m)
    for n in names:
        data = db.medice.insert_one({'name': n})
        print('success...')
