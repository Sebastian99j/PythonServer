from passlib.context import CryptContext

pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(self: str):
        return pwd_hash.hash(self)