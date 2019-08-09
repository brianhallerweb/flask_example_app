from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "obie"
api = Api(app)

# this will created all the tables unless they already exist
# this is a method from flask
@app.before_first_request
def create_tables():
    db.create_all()

# this creates a /auth endpoint
# the client sends username and password to /auth
# /auth runs the authenticate function, which checks username and password in
# the db and then returns a jwt
# /auth requires a POST with username and password in a json body
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')

api.add_resource(Item, '/item/<string:name>')

api.add_resource(StoreList, '/stores')

api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')

# why do this name = main thing?
# if you wanted to import something from app.py into another file, it would run
# the app.py file, which would be a problem if it also started the server. In
# that situation, __name__ is not __main__ so the server won't start.
if __name__ == '__main__':
    # why is this imported here?
    # models and resources will need db because they do sql queries
    # so if db was imported above, it would be imported twice, which would
    # cause problems
    from db import db
    db.init_app(app)
    app.run(port=5050, debug=True)
