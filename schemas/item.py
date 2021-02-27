from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = (
            "store",
        )  # means just use password field on load(POST, request body) not dump(GET, response body)
        dump_only = ("id",)  # return it only (used in GET) ==> dump_only=True
        include_fk = True  # store_id
