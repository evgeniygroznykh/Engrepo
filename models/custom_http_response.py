from flask import Response


class CustomResponse(Response):
    charset = 'utf-16'