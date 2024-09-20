from flask import request
from flask_restx import Namespace, Resource

from api.extensions import db
from api.utils.jwt import token_required
from api.utils.response import CommonResponse

from .user_dto import update_user_dto
from .user_models import User
from .user_schema import UserSchema

user_controller = Namespace("api/v4/users")


@user_controller.route("/me")
class Me(Resource):
    @token_required
    def get(self, data):
        user_id = data["id"]
        user = User.query.get(user_id)

        if not user:
            return CommonResponse.not_found("User not found")

        user_scheme = UserSchema()
        return CommonResponse.read(user_scheme.dump(user))


@user_controller.route("/")
class All(Resource):
    def get(self):
        list_users = User.query.all()
        user_scheme = UserSchema(many=True)
        users_json = user_scheme.dump(list_users)
        return CommonResponse.read(users_json)


@user_controller.route("/<int:id>")
class Detail(Resource):
    @token_required
    def get(self, data, id):
        user = User.query.get(id)

        if not user:
            return CommonResponse.not_found("User not found")

        user_scheme = UserSchema()
        return CommonResponse.read(user_scheme.dump(user))

    @token_required
    @user_controller.expect(update_user_dto, validate=True)
    def patch(self, data, id):
        if id != data["id"]:
            return CommonResponse.forbidden("You don't have access")

        user = User.query.get(id)
        if not user:
            return CommonResponse.not_found("User not found")

        form = request.get_json()
        user.name = form.get("name")
        db.session.commit()
        return CommonResponse.update(UserSchema().dump(user))

    @token_required
    def delete(self, data, id):
        if id != data["id"]:
            return CommonResponse.forbidden("You don't have access")

        user = User.query.get(id)
        if not user:
            return CommonResponse.not_found("User not found")

        db.session.delete(user)
        db.session.commit()
        return CommonResponse.delete("delete user success")
