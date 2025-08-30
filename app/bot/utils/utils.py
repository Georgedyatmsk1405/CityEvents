from aiogram.types import Message


async def greet_user(message: Message, is_new_user: bool) -> None:
    """
    Приветствует пользователя и отправляет соответствующее сообщение.
    """
    greeting = "Добро пожаловать" if is_new_user else "Привет"

    await message.answer(
        f"""{greeting}, Как хотите провести время?""",
    )
