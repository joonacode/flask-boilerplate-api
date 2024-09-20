from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .blog_models import Blog


class BlogUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blog
        load_instance = True
        include_relationships = True
        exclude = [
            "user.status",
            "user.token",
            "user.email",
            "user.created_at",
            "user.updated_at",
        ]

    from ..user.user_schema import UserSchema

    user = fields.Nested(UserSchema)


class BlogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blog
        load_instance = True
