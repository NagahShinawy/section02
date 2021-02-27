from marshmallow import Schema, fields, validates, ValidationError
from models.user import UserModel
from errors.messages import USER_ALREADY_EXISTS
from ma import ma

# class UserSchema(Schema):
#     # id = fields.Int(dump_only=True)  # return it only (used in GET) ==> dump_only=True
#     id = fields.Int()  # you can add dump only at class Meta
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)
#
#     class Meta:
#         load_only = ("password", )  # means just use password field on load(POST) not dump(GET)
#         dump_only = ("id", )  # return it only (used in GET) ==> dump_only=True
#
#     # @validates("username")
#     # def validate_username(self, value):
#     #     user = UserModel.find_by_username(value)
#     #     if user:
#     #         raise ValidationError(USER_ALREADY_EXISTS)
#     #     return value


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = (
            "password",
        )  # means just use password field on load(POST, request body) not dump(GET, response body)
        dump_only = (
            "id",
            "activated",
        )  # return it only (used in GET) ==> dump_only=True
