from urllib import response
from flask import Blueprint, Response
from application.db.db import dbConnection
from bson import ObjectId, json_util

db = dbConnection()


medicines_bp = Blueprint('medicines', __name__ , url_prefix= '/api/v1/medicines')


#Route for consult all medicines 
@medicines_bp.route('/', methods=['POST','GET'])
def get_all_medicines():
    data = db.medice.find()
    response = json_util.dumps(data)
    return Response(response, mimetype='application/json')


#Route for get one medicine for id 
@medicines_bp.route('/<id>', methods=['GET'])
def get_by_id(id):
    medicine = db.medice.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(medicine)
    return Response(response, mimetype='application/json')