import json
import os

import werkzeug
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import BaseConfig
from .extensions import api, db
from .modules.v4.auth.auth_controller import auth_controller
from .modules.v4.blog.blog_controller import blog_controller
from .modules.v4.user.user_controller import user_controller
from .utils.response import CommonResponse, ResponseApi

app = Flask(__name__)

app.config.from_object(BaseConfig)


db.init_app(app)
api.init_app(app)

api.add_namespace(user_controller)
api.add_namespace(blog_controller)
api.add_namespace(auth_controller)
jwt = JWTManager(app)


def handle_not_found(e):
    return CommonResponse.not_found("page not found")

app.register_error_handler(404, handle_not_found)

CORS(app)


@app.before_request
def initialize_database():
    try:
        db.create_all()
    except Exception as e:

        print("> Error: DBMS Exception: " + str(e))

        # fallback to SQLite
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI = (
            "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
        )

        print("> Fallback to SQLite ")
        db.create_all()


@app.after_request
def after_request(response):
    if int(response.status_code) >= 400:
        try:
            response_data = response.get_data(as_text=True)

            if response_data:
                response_data = json.loads(response_data)

                error = "app error"
                message = "app error"
                if "errors" in response_data:
                    error = response_data["errors"]
                    if "message" in response_data:
                        message = response_data["message"]
                elif "error" in response_data:
                    error = response_data["error"]
                    if "message" in response_data:
                        message = response_data["message"]

                response_data = ResponseApi(
                    status_code=response.status_code,
                    status="FAIL",
                    message=message,
                    data=None,
                    error=error,
                )
                response.set_data(json.dumps(response_data.to_dict()))

            else:
                response_data = ResponseApi(
                    status_code=response.status_code,
                    status="FAIL",
                    message="app error",
                    data=None,
                    error="Unknown error occurred",
                )
                response.set_data(json.dumps(response_data.to_dict()))

        except json.JSONDecodeError:
            # Handle non-JSON responses
            response_data = ResponseApi(
                status_code=response.status_code,
                status="FAIL",
                message="app error",
                data=None,
                error="Json error",
            )
            response.set_data(json.dumps(response_data.to_dict()))

    response.headers.add("Content-Type", "application/json")

    return response
