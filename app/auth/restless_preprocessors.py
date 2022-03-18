from flask_login import current_user
from flask import abort


def auth_preprocessor(filters=None, **kw):
    """
    Preprocessor used to validate if a user is authenticated.

    We set this preprocessor in the constructor of the APIManager to be executed for all APIs.
    :param filters:
    :param kw:
    :return:
    """
    if not current_user.is_authenticated:
        raise abort(401)


auth_preprocessors = {
    'GET_COLLECTION': [auth_preprocessor],
    'GET_RESOURCE': [auth_preprocessor],
    'GET_RELATION': [auth_preprocessor],
    'GET_RELATED_RESOURCE': [auth_preprocessor],
    'DELETE_RESOURCE': [auth_preprocessor],
    'POST_RESOURCE': [auth_preprocessor],
    'PATCH_RESOURCE': [auth_preprocessor],
    'GET_RELATIONSHIP': [auth_preprocessor],
    'DELETE_RELATIONSHIP': [auth_preprocessor],
    'POST_RELATIONSHIP': [auth_preprocessor],
    'PATCH_RELATIONSHIP': [auth_preprocessor],
}


def user_api_preprocessor(filters=None, **kw):
    """
    Preprocessor for User API so each user can see/modify only his/her own data.

    :param filters:
    :param kw:
    :return:
    """
    if 'resource_id' not in kw or kw['resource_id'] != current_user.get_id():
        raise abort(401)


user_api_preprocessors = {
    'GET_COLLECTION': [user_api_preprocessor],
    'GET_RESOURCE': [user_api_preprocessor],
    'GET_RELATION': [user_api_preprocessor],
    'GET_RELATED_RESOURCE': [user_api_preprocessor],
    'DELETE_RESOURCE': [user_api_preprocessor],
    'POST_RESOURCE': [user_api_preprocessor],
    'PATCH_RESOURCE': [user_api_preprocessor],
    'GET_RELATIONSHIP': [user_api_preprocessor],
    'DELETE_RELATIONSHIP': [user_api_preprocessor],
    'POST_RELATIONSHIP': [user_api_preprocessor],
    'PATCH_RELATIONSHIP': [user_api_preprocessor],
}
