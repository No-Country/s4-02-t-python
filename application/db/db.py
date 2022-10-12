# Mongo URI
from pymongo import MongoClient


MONGO_URI = 'mongodb+srv://hermes:jm9Sp2lBKEqHSV2i@hermes.awnisit.mongodb.net/?retryWrites=true&w=majority'


def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client['users']
        print('conexion success')
    except ConnectionError:
        print('Error de conexion')

    return db

