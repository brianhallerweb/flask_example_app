import sqlite3
from flask_restful import Resource
from flask import request
from models.user import UserModel

class UserRegister(Resource):

    def post(self):
        username = request.json['username']
        password = request.json['password']
        
        if UserModel.find_by_username(username):
            return {'message': f'user {username} already exists'}, 400 

        new_user = UserModel(username, password)

        try:
            new_user.save_to_db()
        except:
            return {'message': f'error adding new user {username}'}, 500

        return {'message': f'user {username} created successfully'}, 201

