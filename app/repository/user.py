from app.models import User
from app.repository.base import BaseRepo


class UserRepo(BaseRepo):
    model = User
