from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # this line tells sql alchemy there is a relationship between StoreModel
    # and ItemModel
    # I guess it looks in the same directory for ItemModel?
    # What kind of relationship?
    # sqlqlchemy will see that each item has a store_id as a foreign key
    # stores has a one-to-many relationship with items (one store, many items)
    # So "items" is a list
    items = db.relationship('ItemModel');

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

