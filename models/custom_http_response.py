from flask import Response


class CustomHttpResponse(Response):
    charset = 'utf-16'
