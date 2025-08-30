from app.models import Message
from app.repository.base import BaseRepo


class MessageRepo(BaseRepo):
    model = Message
