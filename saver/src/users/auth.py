from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password_from_user: str, password_in_database: str) -> bool:
    return password_context.verify(password_from_user, password_in_database)