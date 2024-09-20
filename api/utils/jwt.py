from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import request

from api.config import BaseConfig
from api.utils.response import CommonResponse


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return CommonResponse.forbidden("Token required")

        try:
            data = DecodeJwt(token).access_token()
            return f(*args, data=data, **kwargs)

        except TokenError as e:
            return e.return_error()

    return decorator


class GenerateToken:
    def __init__(self, id):
        self.id = id

    def access_token(self):
        token = jwt.encode(
            {
                "id": self.id,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            },
            BaseConfig.SECRET_KEY,
        )
        return token

    def create_account_token(self):
        token = jwt.encode(
            {
                "id": self.id,
                "type": 0,
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
            },
            BaseConfig.SECRET_KEY_ACCOUNT,
        )
        return token

    def forgot_password_token(self):
        token = jwt.encode(
            {
                "id": self.id,
                "type": 1,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            },
            BaseConfig.SECRET_KEY_ACCOUNT,
        )
        return token

    def refresh_token(self):
        refresh_token = jwt.encode(
            {
                "id": self.id,
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            },
            BaseConfig.SECRET_KEY_REFRESH,
        )
        return refresh_token


class TokenError(Exception):
    """Custom exception for token-related errors."""

    def __init__(self, message, status_code=401):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def return_error(self):
        if self.status_code == 401:
            return CommonResponse.unauthorized(self.message)
        elif self.status_code == 403:
            return CommonResponse.forbidden(self.message)
        else:
            return CommonResponse.bad_request(self.message)


class DecodeJwt:
    def __init__(self, token):
        self.token = token

    def generate(self, config):
        try:
            data = jwt.decode(self.token, config, algorithms=["HS256"])
            return data
        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired", status_code=401)
        except jwt.InvalidTokenError:
            raise TokenError("Token invalid", status_code=401)
        except Exception as e:
            print("Error: " + str(e))
            raise TokenError("Error when decoding token", status_code=401)

    def access_token(self):
        return self.generate(BaseConfig.SECRET_KEY)

    def refresh_token(self):
        return self.generate(BaseConfig.SECRET_KEY_REFRESH)

    def account_token(self):
        return self.generate(BaseConfig.SECRET_KEY_ACCOUNT)
