from urllib import response
from flask import Blueprint, Response, request, jsonify, session
from sqlalchemy import true
from application.db.db import dbConnection
from bson import ObjectId, json_util

db = dbConnection()

meetings_bp = Blueprint('meetings', __name__ , url_prefix= '/api/v1/meetings')


# create a meeting
@meetings_bp.route('/<id>', methods=['POST'])
def create_meeting(id):
    post = db.posts.find_one({'_id': ObjectId(id)})
    post_id = json_util.dumps(post)
    date = request.json['date']
    user = session['user_id']
    user_id = db.users.find_one({'_id': ObjectId(user)})
    first_name = user_id['first_name']
    last_name = user_id['last_name']
    

    if date:
        user_id = session['user_id']
        print(user_id)
        id = db.meetings.insert_one(
            {'date': date, 'post_id': post_id, 'user_id': [first_name, last_name]}
        )
        
        response = jsonify({
            'id': str(id),
            'date': date,
            'post_id': post_id,
            'user_id': [first_name,last_name]
        })
        response.status_code = 201
        print(response)
        
        return response
    else:
        return jsonify({'error': 'there is a wrong'}), 400    


@meetings_bp.route('/all', methods=['GET'])
def get_all_meeting():
    meetings = db.meetings.find()
    # print(users)
    response = json_util.dumps(meetings)
    return Response(response, mimetype='application/json')


@meetings_bp.route('/<id>', methods=['GET'])
def get_meeting(id):
    meeting = db.meetings.find_one({'_id': ObjectId(id)})
    if meeting:
        response = json_util.dumps(meeting)
        # response.status_code = 200
        print(meeting)
        return Response(response, mimetype='application/json')
    else:
        return jsonify({'error': 'Meeting not found'}), 404


@meetings_bp.route('/update/<id>', methods=['PUT'])
def update_meeting(id):
    meeting = db.meetings.find_one({'_id': ObjectId(id)})
    post_id = meeting['post_id']
    date = request.json['date']
    user = session['user_id']
    user_id = db.users.find_one({'_id': ObjectId(user)})
    first_name = user_id['first_name']
    last_name = user_id['last_name']

    if date and post_id:
        user_id = session['user_id']
        id = db.meetings.update_one({'_id': ObjectId(id)},
            {'$set':{'date': date}}
        )
        
        response = jsonify({
            'id': str(id),
            'date': date,
            'post_id': post_id,
            'user_id': [first_name,last_name]
        })
        response.status_code = 200
        print(response)
        
        return response
    else:
        return jsonify({'error': 'error'}), 400