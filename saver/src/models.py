from sqlalchemy import text, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from typing import Annotated


str_null = Annotated[str, mapped_column(nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))


    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()[:-5] + 's'


class UserModel(Base):
    __table_args__ = {'extend_existing': True}
    
    username: Mapped[str_null]
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str_null]
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    

class ExpenseModel(Base):
    __table_args__ = {'extend_existing': True}
    
    #user_id: Mapped[int] = mapped_column(foreing_key=UserModel.id)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String)