from flask_restx import fields
from api.extensions import api

create_blog_dto = api.model(
    "CreateBlogDto",
    {
        "title": fields.String(required=True, min_length=2, max_length=32),
        "content": fields.String(required=True, min_length=4, max_length=64),
    },
)

update_blog_dto = api.model(
    "UpdateBlogDto",
    {
        "title": fields.String,
        "content": fields.String,
    },
)
