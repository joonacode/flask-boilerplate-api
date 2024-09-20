from flask_restx import fields

from api.extensions import api

signup_dto = api.model(
    "SignUpDto",
    {
        "name": fields.String(required=True, min_length=2, max_length=32),
        "email": fields.String(required=True, min_length=4, max_length=64),
        "password": fields.String(required=True, min_length=4, max_length=16),
    },
)

login_dto = api.model(
    "LoginDto",
    {
        "email": fields.String,
        "password": fields.String,
    },
)

activate_account_dto = api.model(
    "ActivateAccountDto",
    {
        "token": fields.String(required=True, min_length=2),
    },
)

refresh_token_dto = api.model(
    "RefreshTokenDto",
    {
        "refresh_token": fields.String(required=True, min_length=2),
    },
)

forgot_password_dto = api.model(
    "ForgotPasswordDto",
    {
        "email": fields.String(required=True, min_length=2),
    },
)

reset_password_dto = api.model(
    "ResetPasswordDto",
    {
        "token": fields.String(required=True, min_length=2),
        "password": fields.String(required=True, min_length=8),
        "verify_password": fields.String(required=True, min_length=8),
    },
)
