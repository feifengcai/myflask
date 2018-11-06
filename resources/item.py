import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="field is required")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        #item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)		
        print(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error in inserting item."}, 500 # internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "item '{}' is deleted.".format(name)}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        status = 200
        if item and item.price == data['price']:
            return {'message': "Nothing to update."}, status

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            status = 201
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json(), status


class ItemList(Resource):
    def get(self):
        #return {'items': list(map(lambda x:x.json(), ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}
    '''
    def get(self):
        items = ItemModel.query.all()
        print ("----", type(items), items)
        r = []
        for x in items:
            print("----", type(x), x, x.json())
            print("----", x.name, x.price)
            r.append(x.json())
        print ("----", r)
        return {'items': r}
        '''




