from application.db.db import dbConnection

db = dbConnection()

with open('medicamentos.txt', 'r', encoding='utf-8') as m:
    lineas = m.readlines()
    lineas = list(map(lambda l: l.strip('\n'), lineas))
    for l in lineas:
        data = db.medice.insert_one({'name': l})
        print('success...')
