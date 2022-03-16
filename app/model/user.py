from flask_login import UserMixin
from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.orm import relationship

from app.database import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    # Using with_variant enables auto_increment in sqlite
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String, unique=True)

    credentials = relationship("UserCredential", back_populates='user', cascade="all, delete")
