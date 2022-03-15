from app.database import db
from app.model.user import User
from app.model.user_credential import UserCredential


def find_by_username(username: str):
    return UserCredential.query \
        .join(User) \
        .filter(User.name == username).all()


def save_credential(user: User, name: str, credential_base64: str):
    new_credential = UserCredential(name=name, base64=credential_base64, user=user)
    db.session.add(new_credential)
