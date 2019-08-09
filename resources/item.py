from flask_restful import Resource
from flask import request
from flask_jwt import JWT, jwt_required
from models.item import ItemModel

# Resources normally use models to interact data from db

class Item(Resource):
    # jwt_required is a decorator
    # it just means that sending a jwt is required for calling get method
    # you send the token as a header with key=Authorization and value=JWT
    # <token_number> (meaning you have to write "JWT" then " " then paste the
    # token number)
    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {'message': f'item {name} not found'}, 404

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'item {name} already exists'}, 400 

        price = request.json['price']
        store_id = request.json['store_id']

        item = ItemModel(name, price, store_id)

        try:
            item.save_to_db()
        except:
            return {'message': f'error posting item {name}'}, 500

        return {'message': f'item {name} added successfully'}, 201

    # @jwt_required()
    def put(self, name):
        updated_price = request.json['price']
        store_id = request.json['store_id']
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = updated_price
                item.save_to_db()
                return item.json()
            except:
                return {'message': f'An error occurred updating item {name}'}, 500 
        else:
            try:
                item = ItemModel(name, updated_price, store_id)
                item.save_to_db()
                return item.json()
            except:
                return {'message': f'An error occurred inserting item {name}'},500 
                

    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db(name)
            return {'message': f'item {name} deleted successfully'}
        else:
            return {'message': f'item does not exist'}, 400 


class ItemList(Resource):
    
    # @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        

