from pydantic import BaseModel, EmailStr, Field


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(..., description="User E-mail")
    password: str = Field(..., min_length=6, max_length=50, description="The user's password is from 6 characters to 50")


class UserRegisterSchema(UserAuthSchema):
    username: str = Field(..., min_length=2, max_length=50, description="Username consisting of 2 to 50 characters")


class ExpenseSchema(BaseModel):
    amount: int
    description: str
