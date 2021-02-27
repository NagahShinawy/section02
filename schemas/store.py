from ma import ma
from models.store import StoreModel
from schemas.item import ItemSchema


class StoreSchema(ma.ModelSchema):
    # items nested (ma.Nested) in store and contains many items schema (many=True)
    # dump not load
    items = ma.Nested(ItemSchema, many=True)  # ONE store contains MANY items nested in it

    class Meta:
        model = StoreModel
        dump_only = ("id",)  # return it only (used in GET) ==> dump_only=True
