from flask import redirect, Blueprint
from flask_login import LoginManager, login_required, logout_user

from app.model.user import User

login_blueprint = Blueprint('login_blueprint', __name__, url_prefix='/login')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/auth.html')