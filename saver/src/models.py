from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from database import Base

int_pk = Annotated[int, mapped_column(primary_key=True), mapped_column(index=True)]
str_unq = Annotated[str, mapped_column(unique=True)]


class UserModel(Base):
    __tablename__ = "user"
    
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_unq]
    password: Mapped[str]
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_student: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_teacher: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

class ExpenseModel(Base):
    __tablename__ = "expense"
    
    id: Mapped[int_pk]
    amount: Mapped[int]
    description: Mapped[str]