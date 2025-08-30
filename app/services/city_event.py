from aiogram.types import Message

from app.repository.message import MessageRepo
from app.repository.user import UserRepo
from app.services.llm_service import LLMService


class CityEventService:
    @staticmethod
    async def find_events(message: Message):
        text, current_user_id = message.text, message.from_user.id
        user = await UserRepo.find_one_or_none(telegram_id=current_user_id)
        if not user:
            user = await UserRepo.add(
                telegram_id=current_user_id, username=message.from_user.username
            )
        messages = await MessageRepo.find_last_n(limit=10, user_id=current_user_id)
        await MessageRepo.add(user=user, text=text)
        # context = f"""
        # Контекст переписки - последние сообщения:
        # {[m.text for m in messages]}
        # Запрос текущий - {text}
        # """
        # llm_answer = LLMService.get_answer(context, "system")
        # return llm_answer
        return "запрос принят"
