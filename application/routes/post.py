from flask import Blueprint, Response, jsonify, request, session
from application.db.db import dbConnection
from datetime import datetime
from bson import ObjectId, json_util


post_bp = Blueprint('post', __name__, url_prefix='/api/v1/post')

# connection to db
db = dbConnection()


# create a post
@post_bp.route('/create_post', methods=['POST'])
def create_post():
    publication_type = request.json['publication_type']
    publication_date = datetime.now().strftime("%d/%m/%Y")
    image = request.json["image"]
    drug_name = request.json["drug_name"]
    description = request.json["description"]
    presentation = request.json["presentation"]
    meeting_place = request.json["meeting_place"]

    if publication_type and image and drug_name and description and presentation and meeting_place:
        id = session['user_id']
        print(id)
        author_data = db.users.find_one({'_id': ObjectId(id)})
        author_first_name = author_data['first_name']
        author_last_name = author_data['last_name']
        data = db.posts.insert_one({
            'author': author_first_name + ' ' + author_last_name,
            'publication_type': publication_type,
            'publication_date': publication_date,
            'image': image,
            'drug_name': drug_name,
            'description': description,
            'presentation': presentation,
            'meeting_place': meeting_place

        })
        message = jsonify({'message': 'Post created successfully...'})
        return message
    else:
        message = jsonify({"some data is incomplete or incorrect..."})
        return message


# find all post
@post_bp.route('/', methods=['GET'])
def get_all_post():
    data = db.posts.find()
    response = json_util.dumps(data)
    response.status_code = 200
    return Response(response, mimetype='application/json')


# find post by id
@post_bp.route('/<id>', methods=['GET'])
def get_post_by_id(id):
    data = db.posts.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(data)
    return Response(response, mimetype='application/json')


# update post by id
@post_bp.route('/<id>', methods=['PUT'])
def update_post_by_id(id):
    post = db.posts.find_one({'_id': ObjectId(id)})
    publication_type = request.json['publication_type']
    publication_date = datetime.now().strftime("%d/%m/%Y")
    image = request.json["image"]
    drug_name = request.json["drug_name"]
    description = request.json["description"]
    presentation = request.json["presentation"]
    meeting_place = request.json["meeting_place"]

    if publication_type and image and drug_name and description and presentation and meeting_place:
        id = db.posts.update_one({'_id': ObjectId(id)}, {'$set': {
            'author': session['user_id'],
            'publication_type': publication_type,
            'publication_date': publication_date,
            'image': image,
            'drug_name': drug_name,
            'description': description,
            'presentation': presentation,
            'meeting_place': meeting_place
            }})
        message = jsonify({'message': 'Post updated successfully...'})
        return message
    else:
        message = jsonify({"some data is incomplete or incorrect..."})
        return message


# delete post by id
@post_bp.route('/<id>', methods=['DELETE'])
def delete_post_by_id(id):
    data = db.posts.delete_one({'_id': ObjectId(id)})
    message = jsonify({'message': "Post " + id + " was delete successfully"})
    return message
