from aiogram import Router
from aiogram.filters import CommandStart

from aiogram.types import Message


from app.repository.user import UserRepo

from app.bot.utils.utils import greet_user

from app.services.city_event import CityEventService

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    user = await UserRepo.find_one_or_none(telegram_id=message.from_user.id)
    if not user:
        await UserRepo.add(
            telegram_id=message.from_user.id, username=message.from_user.username
        )
    await greet_user(message, is_new_user=not user)


@user_router.message()
async def cmd_answer(message: Message) -> None:
    answer = await CityEventService.find_events(message)
    await message.answer(answer)
