from flask_login import current_user
from flask_restx import Namespace, Resource

api = Namespace('user', description='User operations using RestX')


@api.route('/me')
class User(Resource):
    def get(self):
        return {
            "id": current_user.get_id(),
            "name": current_user.name
        }
