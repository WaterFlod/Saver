from sqlalchemy import text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import Annotated
from pydantic import EmailStr


str_null = Annotated[str, mapped_column(nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))


    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()[:-5] + 's'


class UserModel(Base):
    __table_args__ = {'extend_existing': True}
    
    username: Mapped[str_null]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_null]
    count_expenses: Mapped[int] = mapped_column(server_default=text('0'), nullable=False)
    
    is_user: Mapped[bool] = mapped_column(server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(server_default=text('false'), nullable=False)
    

class ExpenseModel(Base):
    __table_args__ = {'extend_existing': True}
    
    expense_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str]