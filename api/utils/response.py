from http import HTTPStatus

from flask import jsonify, make_response


class ResponseApi:
    def __init__(self, status_code, status, message, data=None, error=None):
        self.status_code = status_code
        self.status = status
        self.message = message
        self.data = data
        self.error = error

    def to_dict(self):
        result = {
            "status_code": self.status_code,
            "status": self.status,
            "message": self.message,
        }
        if self.data is not None:
            result["data"] = self.data
        if self.error is not None:
            result["error"] = self.error
        return result


class CommonResponse:
    @staticmethod
    def ok(data):
        response = ResponseApi(
            status_code=HTTPStatus.OK.value,
            status="OK",
            message="fetch data success",
            data=data,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.OK)

    @staticmethod
    def read(data):
        response = ResponseApi(
            status_code=HTTPStatus.OK.value,
            status="OK",
            message="get data success",
            data=data,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.OK)

    @staticmethod
    def create(data):
        response = ResponseApi(
            status_code=HTTPStatus.CREATED.value,
            status="OK",
            message="create data success",
            data=data,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.CREATED)

    @staticmethod
    def update(data):
        response = ResponseApi(
            status_code=HTTPStatus.OK.value,
            status="OK",
            message="update data success",
            data=data,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.OK)

    @staticmethod
    def delete(data):
        response = ResponseApi(
            status_code=HTTPStatus.OK.value,
            status="OK",
            message="delete data success",
            data=data,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.OK)

    @staticmethod
    def conflict(error):
        response = ResponseApi(
            status_code=HTTPStatus.CONFLICT.value,
            status="FAIL",
            message="conflict",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.CONFLICT)

    @staticmethod
    def not_found(error):
        response = ResponseApi(
            status_code=HTTPStatus.NOT_FOUND.value,
            status="FAIL",
            message="not found",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.NOT_FOUND)

    @staticmethod
    def internal_server_error(error):
        response = ResponseApi(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            status="FAIL",
            message="internal server error",
            error=error,
        )
        return make_response(
            jsonify(response.to_dict()), HTTPStatus.INTERNAL_SERVER_ERROR
        )

    @staticmethod
    def unsupported_media_type(error):
        response = ResponseApi(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
            status="FAIL",
            message="Unsupported media type",
            error=error,
        )
        return make_response(
            jsonify(response.to_dict()), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        )

    @staticmethod
    def bad_request(error):
        response = ResponseApi(
            status_code=HTTPStatus.BAD_REQUEST.value,
            status="FAIL",
            message="bad request",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.BAD_REQUEST)

    @staticmethod
    def unauthorized(error):
        response = ResponseApi(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            status="FAIL",
            message="unauthorized",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.UNAUTHORIZED)

    @staticmethod
    def forbidden(error):
        response = ResponseApi(
            status_code=HTTPStatus.FORBIDDEN.value,
            status="FAIL",
            message="forbidden",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.FORBIDDEN)

    @staticmethod
    def bad_gateway(error):
        response = ResponseApi(
            status_code=HTTPStatus.BAD_GATEWAY.value,
            status="FAIL",
            message="Bad gateway",
            error=error,
        )
        return make_response(jsonify(response.to_dict()), HTTPStatus.BAD_GATEWAY)
