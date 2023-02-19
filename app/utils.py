from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

#hashing of password
def hash(password: str):
    return pwd_context.hash(password)


#verify passowrd
def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)