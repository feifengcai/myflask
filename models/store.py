from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #items = db.relationship('ItemModel', lazy='dynamic')
    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def json(self):
        #return {'name': self.name, 'items': [x.json() for x in self.items.all()]}
        return {'name': self.name, 'items': [x.json() for x in self.items]}

    @classmethod
    def find_by_name(cls, name):
        r = cls.query.filter_by(name=name).first() # "SELECT * FROM items WHERE name=name LIMIT 1"
        print("----", type(r))
        return r

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
