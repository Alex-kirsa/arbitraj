from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, VARCHAR, TIMESTAMP, FLOAT, TEXT, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from bot.db.base import Base
from bot.utils.constants import RoleTypes


class Users(Base):
    __tablename__ = "users"

    user_id = mapped_column(BIGINT, primary_key=True)
    username = mapped_column(VARCHAR(255), nullable=True, doc='Username в Telegram', name='Username в Telegram')
    fullname = mapped_column(VARCHAR(255), nullable=False)
    role = mapped_column(Enum(RoleTypes), nullable=True, doc='Роль пользователя', name='Роль пользователя')
    balance = mapped_column(FLOAT, nullable=False, doc='Баланс пользователя', name='Баланс пользователя', default=0)


