from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .user_models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ["password"]
