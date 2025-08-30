from sqlalchemy import String, BigInteger, ForeignKey, Text, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с сообщениями
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")


class Message(Base):
    __tablename__ = "messages"  # Исправлено имя таблицы

    id = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)  # Исправлен тип на Text

    # Внешний ключ на пользователя
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE")
    )

    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="messages")
