from flask import Blueprint, g
from flask import jsonify, request, Response, session
from application.db.db import dbConnection
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, json_util

# we create a Blueprint for users route
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')


# we create a db conection
db = dbConnection()


@user_bp.route('/register', methods=['POST'])
def create_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    country = request.json['country']
    city = request.json['city']
    #agregar foto de usuario


    if last_name and email and country and password and first_name and city:
        hashed_password = generate_password_hash(password)
        
        if db.users.find_one({'email': email}):
            return jsonify({'error': 'Email address already in use'})

        id = db.users.insert_one(
            {'first_name':first_name, 'last_name': last_name, 'email': email, 'password': hashed_password, 'country': country, 'city': city}
        )
        
        response = jsonify({
            'id': str(id),
            'first_name': first_name,
            'last_name': last_name,
            'password': hashed_password,
            'email': email,
            'country': country,
            'city': city
        })
        response.status_code = 201
        return response
    else:
        return jsonify({'error': 'Signup failed maybe some fields are incomplete'}), 400
    # return {'messaje': 'received'}


@user_bp.route('/', methods=['GET'])
def get_users():
    users = db.users.find()
    # print(users)
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@user_bp.route('/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


@user_bp.route('/<id>', methods=['PUT'])
def update_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    country = request.json['country']
    city = request.json['city']

    if first_name and last_name and email and country and password:
        hashed_password = generate_password_hash(password)
        db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'first_name': first_name, 
            'last_name': last_name, 
            'email': email, 
            'password': hashed_password, 
            'country': country,
            'city': city
            }})
        response = jsonify({'message': 'User ' + id + ' was updated successfully'})

        return response
    else:
        return jsonify({'message': 'Some fields without information'})
    

@user_bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' was deleted successfully'})
    response.status_code = 200
    return response


@user_bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    # verify if email exist
    user = db.users.find_one({"email": email})
    if user:
        # Verify password match
        if check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            print(session)
            return jsonify({'message': "User loging successfull..."})
        else:
            return jsonify({'message': 'Invalid crendentials'})
    else:
        response = jsonify({'message': 'Invalid credentials'})
        response.status_code = 404
        return response

@user_bp.route('/logout')
def logout():
	if 'user_id' in session:
		session.pop('username', None)
	return jsonify({'message' : 'You successfully logged out'})

@user_bp.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response




