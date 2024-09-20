from flask_restx import fields

from api.extensions import api

update_user_dto = api.model(
    "UpdateUserDto",
    {
        "name": fields.String(required=True, min_length=2, max_length=32),
    }
)
