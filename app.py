from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
        
    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

#create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = Users(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating user'}), 500)

#get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting list of all users'}), 500)
    
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = Users.query.filter_by(id=id).first()
        return make_response(jsonify({'user': user.json()}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error retrieving user'}), 500)
    
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'failed to update user'}), 500)
    
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'failed to delete user'}), 500)
    

    

    

