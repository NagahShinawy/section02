from marshmallow import Schema, fields, validates, ValidationError
from models.user import UserModel
from errors.messages import USER_ALREADY_EXISTS


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # return it only (used in GET) ==> dump_only=True
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    class Meta:
        fields = ("id", "username")  # just include id, username

    # @validates("username")
    # def validate_username(self, value):
    #     user = UserModel.find_by_username(value)
    #     if user:
    #         raise ValidationError(USER_ALREADY_EXISTS)
    #     return value