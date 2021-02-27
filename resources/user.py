from flask_restful import Resource
from flask import request, make_response, render_template
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from marshmallow import ValidationError

from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from errors.messages import (
    USER_ALREADY_EXISTS,
    CREATED_SUCCESSFULLY,
    USER_NOT_FOUND,
    USER_DELETED,
    INVALID_CREDENTIALS,
    USER_LOGGED_OUT,
    NOT_CONFIRMED_USER,
    USER_CONFIRMED,
)

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        # user_data : is dictionary or user obj based on coding of Schema
        # if you are inherit from Schema ==> user_data is dictionary
        # if you are inherit from ModelSchema ==> user_data is user obj
        user_data = user_schema.load(
            request.get_json()
        )  # shift + f6 to update all usages of variable
        # try:
        #     user_data = user_schema.load(
        #         request.get_json()
        #     )  # shift + f6 to update all usages of variable
        # todo : use @app.errorhandler(ValidationError) instead
        # except ValidationError as err:  # errors comes from marshmallow validations
        #     return err.messages, 400

        # if UserModel.find_by_username(user_data["username"]):
        #     return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_username(user_data.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        # user = UserModel(**user_data)  (old) when using Schema not ModelSchema

        # no need UserModel because we are using nullable=False for username and password
        # user = UserModel(username=user_data.username, password=user_data.password)
        user_data.save_to_db()  # user_data is now user obj not dictionary

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user_schema.dump(user)
        # return user.json(), 200 (old)
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # user_data : is dictionary or user obj based on coding of Schema
        # if you are inherit from Schema ==> user_data is dictionary
        # if you are inherit from ModelSchema ==> user_data is user obj
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        # try:
        #     user_json = request.get_json()
        #     user_data = user_schema.load(user_json)
        #  todo : use @app.errorhandler(ValidationError) instead
        # except ValidationError as err:
        #     return err.messages, 400

        # user = UserModel.find_by_username(user_data["username"])
        user = UserModel.find_by_username(user_data.username)

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, user_json.get("password")):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                return {"message": NOT_CONFIRMED_USER.format(user.username)}, 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.activated = True
        user.save_to_db()
        # return {"message": USER_CONFIRMED.format(user.username)}, 200
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=user.username), 200, headers)
