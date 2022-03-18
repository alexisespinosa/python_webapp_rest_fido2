from flask_restx import Api

from app.auth.restx_decorators import auth_decorator
from app.apis.user import api as user_ns


api = Api(prefix='/api', decorators=[auth_decorator], doc='/api/doc')

api.add_namespace(user_ns)
