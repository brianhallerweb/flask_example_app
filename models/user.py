from db import db

# what are models? How do they differ from resources?
# He says models are internal representations of an entity and resources are
# external representations of an entity
# When the client interacts with the API, they are dealing with resources.
# Models are just stuctures for internal use. 
# You could also think of the model as a helper to the resource that doesn't
# pollute the cleanliness of the resource.

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


