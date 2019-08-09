from flask_restful import Resource
from flask import request
from flask_jwt import JWT, jwt_required
from models.store import StoreModel

class Store(Resource):

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': f'store {name} not found'}, 404

    # @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'store {name} already exists'}, 400 

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': f'error creating store {name}'}, 500

        return {'message': f'store {name} added successfully'}, 201


    # @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            StoreModel.delete_from_db(name)
            return {'message': f'store {name} deleted successfully'}
        else:
            return {'message': f'store does not exist'}, 400 


class StoreList(Resource):
    
    # @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
        

