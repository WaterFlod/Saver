from sqlalchemy import text, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Annotated
from datetime import datetime

from database import Base

int_pk = Annotated[int, mapped_column(primary_key=True), mapped_column(index=True)]
str_unq = Annotated[str, mapped_column(unique=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()[:-5] + 's'


class UserModel(Base):
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_unq]
    password: Mapped[str]
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    

class ExpenseModel(Base):
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int_pk]
    #user_id: Mapped[int] = mapped_column(foreing_key=UserModel.id)
    amount: Mapped[int]
    description: Mapped[str]