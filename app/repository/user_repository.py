from app.database import db
from app.model.user import User


def find_by_name(name: str) -> User:
    return User.query.filter(User.name == name).first()


def add_user(name: str):
    new_user = User(name=name)
    db.session.add(new_user)

    return new_user
