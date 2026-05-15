from pwdlib import PasswordHash

pwd_hasher = PasswordHash.recommended()

DUMMY_HASH = pwd_hasher.hash("dummypassword")

def hash_password(plain_password: str) -> str:
    return pwd_hasher.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)