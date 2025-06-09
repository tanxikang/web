from routes import db, login_manager
from sqlalchemy import Identity, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_login import UserMixin
import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def check_password_correction(self, attempted_password):
        password_hashed = self.password.encode()
        return bcrypt.checkpw(attempted_password.encode(), password_hashed)