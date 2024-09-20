from flask import request
from flask_restx import Namespace, Resource
from werkzeug.security import generate_password_hash

from api.extensions import db
from api.utils.jwt import DecodeJwt, GenerateToken, TokenError
from api.utils.response import CommonResponse

from ..user.user_models import User
from .auth_dto import (
    activate_account_dto,
    forgot_password_dto,
    login_dto,
    refresh_token_dto,
    reset_password_dto,
    signup_dto,
)

auth_controller = Namespace("api/v4/auth")


@auth_controller.route("/register")
class Register(Resource):
    @auth_controller.expect(signup_dto, validate=True)
    def post(self):
        form = request.get_json()
        name = form.get("name")
        email = form.get("email")
        password = form.get("password")
        user = User.get_by_email(email)

        if user:
            return CommonResponse.conflict("Email already exists")

        token = GenerateToken(None).create_account_token()
        new_user = User(name=name, email=email, token=token)

        new_user.set_password(password)
        new_user.save()
        # send email to activate account here
        # return CommonResponse.create("Register success")
        return CommonResponse.create({"activate_account_token": token})


@auth_controller.route("/login")
class Login(Resource):
    @auth_controller.expect(login_dto, validate=True)
    def post(self):
        form = request.get_json()
        email = form.get("email")
        password = form.get("password")
        user = User.get_by_email(email)

        if not user:
            return CommonResponse.not_found("Email not found")

        if not user.check_password(password):
            return CommonResponse.unauthorized("Wrong password")

        if user.status == 0:
            return CommonResponse.unauthorized("Please active your account first")

        generate_token = GenerateToken(user.id)

        user.save()
        return CommonResponse.ok(
            {
                "token": generate_token.access_token(),
                "refresh_token": generate_token.refresh_token(),
            }
        )


@auth_controller.route("/activate-account")
class ActivateAccount(Resource):
    @auth_controller.expect(activate_account_dto, validate=True)
    def post(self):
        form = request.get_json()
        token = form.get("token")
        try:
            data = DecodeJwt(token).account_token()
            if data["type"] != 0:
                return CommonResponse.forbidden("Token invalid")

            user = User.get_by_token(token)
            if not user:
                return CommonResponse.not_found("User not found")
            if user.status == 1:
                return CommonResponse.bad_request("Your account already active")
            user.status = 1
            user.token = ""
            db.session.commit()
            return CommonResponse.update("Activate account success")
        except TokenError as e:
            if e.message == "Token expired":
                userx = User.query.filter_by(token=token).first()
                print(f"user {userx}")
                if not userx:
                    return CommonResponse.not_found(
                        "Token not found, please register again"
                    )
                db.session.delete(userx)
                db.session.commit()
                return CommonResponse.delete("token expired please register again")
            else:
                return e.return_error()


@auth_controller.route("/forgot-password")
class ForgotPassword(Resource):
    @auth_controller.expect(forgot_password_dto, validate=True)
    def post(self):
        form = request.get_json()
        email = form.get("email")
        user = User.get_by_email(email)

        if not user:
            return CommonResponse.not_found("Email not found")

        if user.status != 1:
            return CommonResponse.not_found("Make sure your account active first")

        token = GenerateToken(user.id).forgot_password_token()
        # send email to reset password here
        # return CommonResponse.create("Register success")
        return CommonResponse.ok({"reset_password_token": token})


@auth_controller.route("/reset-password")
class ResetPassword(Resource):
    @auth_controller.expect(reset_password_dto, validate=True)
    def post(self):
        form = request.get_json()
        token = form.get("token")
        password = form.get("password")
        verify_password = form.get("verify_password")
        if password != verify_password:
            return CommonResponse.bad_request("password and verify_password different")

        try:
            data = DecodeJwt(token).account_token()
            if data["type"] != 1:
                return CommonResponse.forbidden("Token invalid")

            user = User.query.get(data["id"])
            if not user:
                return CommonResponse.not_found("User not found")

            user.password = generate_password_hash(password)
            user.token = ""
            db.session.commit()
            return CommonResponse.update("Update password success")
        except TokenError as e:
            return e.return_error()


@auth_controller.route("/refresh-token")
class RefreshToken(Resource):
    @auth_controller.expect(refresh_token_dto, validate=True)
    def post(self):
        form = request.get_json()
        refresh_token = form.get("refresh_token")
        try:
            data = DecodeJwt(refresh_token).refresh_token()

            user = User.query.get(data["id"])
            if not user:
                return CommonResponse.not_found("User not found")

            generate_token = GenerateToken(user.id)

            return CommonResponse.ok(
                {
                    "token": generate_token.access_token(),
                    "refresh_token": generate_token.refresh_token(),
                }
            )
        except TokenError as e:
            return e.return_error()
