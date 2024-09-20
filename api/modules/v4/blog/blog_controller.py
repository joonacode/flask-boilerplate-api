from flask import request
from flask_restx import Namespace, Resource

from api.utils.jwt import token_required
from api.utils.response import CommonResponse

from .blog_dto import create_blog_dto, update_blog_dto
from .blog_models import Blog
from .blog_schema import BlogSchema, BlogUserSchema

blog_controller = Namespace("api/v4/blogs")


@blog_controller.route("/")
class All(Resource):
    @token_required
    def get(self, data):
        list_blogs = Blog.get_all()
        blog_schema = BlogUserSchema(many=True)
        blogs_json = blog_schema.dump(list_blogs)
        return CommonResponse.read(blogs_json)

    @blog_controller.expect(create_blog_dto, validate=True)
    @token_required
    def post(self, data):
        form = request.get_json()
        title = form.get("title")
        content = form.get("content")
        new_blog = Blog(title=title, content=content, user_id=data["id"])
        new_blog.save()
        return CommonResponse.create(new_blog.toJSON())


@blog_controller.route("/me")
class AllMe(Resource):
    @token_required
    def get(self, data):
        list_blogs = Blog.get_all_by_user_id(data["id"])
        blog_schema = BlogSchema(many=True)
        blogs_json = blog_schema.dump(list_blogs)
        return CommonResponse.read(blogs_json)


@blog_controller.route("/<int:id>")
class Detail(Resource):
    @token_required
    def get(self, data, id):
        detail = Blog.get_by_id(id)
        if detail is None:
            return CommonResponse.not_found("Blog not found")

        blog_schema = BlogUserSchema()
        return CommonResponse.read(blog_schema.dump(detail))

    @blog_controller.expect(update_blog_dto, validate=True)
    @token_required
    def patch(self, data, id):
        detail = Blog.get_by_id(id)
        if detail is None:
            return CommonResponse.not_found("Blog not found")

        form = request.get_json()
        title = form.get("title")
        content = form.get("content")

        new_blog = Blog(title=title, content=content)
        new_blog.save()

        return CommonResponse.read(new_blog.toJSON())

    @token_required
    def delete(self, data, id):
        detail = Blog.get_by_id(id)
        if detail is None:
            return CommonResponse.not_found("Blog not found")

        if detail.user_id != data["id"]:
            return CommonResponse.forbidden(
                "You don't have permission to delete this blog"
            )

        Blog.delete_by_id(id)
        return CommonResponse.delete("delete success")
