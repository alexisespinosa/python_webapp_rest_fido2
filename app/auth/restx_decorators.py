from flask_login import login_required


def auth_decorator(func):
    """
    This decorator is only to be able to use @login_required decorator from flask_login.
    :param func:
    :return:
    """
    @login_required
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    # Need to pass methods so flask knows which ones are supported.
    # See:
    #   flask_restk.api._register_view line 366
    #   flask.app.add_url_rule line 1055
    wrapper.methods = func.methods
    return wrapper
