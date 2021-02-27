from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema
from marshmallow import ValidationError


NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):

        item = ItemModel.find_by_name(name)
        if item:
            # return item.json(), 200
            return item_schema.dump(item), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        # data = cls.parser.parse_args() (old)
        item_json = request.get_json()
        item_json.update(name=name)
        item = item_schema.load(item_json)
        # try:
        #     item = item_schema.load(item_json)
        # except ValidationError as err:  # todo : use @app.errorhandler(ValidationError) instead
        #     return err.messages, 400
        # item = ItemModel(name=name, price=item_obj.price, store_id=item_obj.store_id) (old)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        # return item.json(), 201 (old)
        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_DELETED}, 404

    @classmethod
    def put(cls, name: str):
        # data = cls.parser.parse_args() (old)
        item_json = request.get_json()
        # item = ItemModel.find_by_name(name=name)
        item = ItemModel.find_by_name_and_store(
            name=name, store_id=item_json.get("store_id")
        )
        if item:
            item.price = item_json["price"]
        else:
            item_json.update({"name": name})
            item = item_schema.load(item_json)
            # try:
            #
            #     item_json.update({"name": name})
            #     item = item_schema.load(item_json)
            # except ValidationError as err:  todo : use @app.errorhandler(ValidationError) instead
            #     return err.messages, 400
        try:
            item.save_to_db()
        except Exception:
            return {"msg": "ERROR_INSERTING"}, 500
        # return item.json(), 200  (old)
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        items = ItemModel.find_all()
        # return {"items": item_schema.dump(items, many=True)}, 200 (it works)
        return {"items": items_schema.dump(items)}, 200
