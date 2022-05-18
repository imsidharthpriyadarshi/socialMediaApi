from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated= "auto")


def hash(password: str):
    return pwd_context.hash(password)

def verifyHashedPaasword(plain_paasword, hashed_paasword):
    return pwd_context.verify(plain_paasword,hashed_paasword)