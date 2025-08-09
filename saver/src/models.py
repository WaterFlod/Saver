from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from database import Base

intpk = Annotated[int, mapped_column(primary_key=True), mapped_column(index=True)]


class ExpenseModel(Base):
    __tablename__ = "expenses"
    
    id: Mapped[intpk]
    amount: Mapped[int]
    description: Mapped[str]