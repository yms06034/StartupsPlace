from flask import Blueprint, g, abort
from flask_restx import Api
from .user import ns as UserNamespace
from functools import wraps

# 어드민만 접근 가능
def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user.user_name == 'admin':
            abort(401)
        return func(*args, **kwargs)
    return __wrapper


blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)

api = Api(
    blueprint,
    title = "성공창업 API",
    version = "1.0",
    doc = "/docs",
    decorators=[check_session],
    description = "Welcome 성공창업 API"
)

api.add_namespace(UserNamespace)
