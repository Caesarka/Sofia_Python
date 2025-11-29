from datetime import datetime, timedelta
import jwt
from config import settings

def create_access_token(claim: dict, expires_minutes: int=None):
    expire = datetime.now() + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE)
    claim.update({"exp": expire})
    encoded_jwt = jwt.encode(claim, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        print("TOKEN = ", token)
        print("SECRET_KEY = ", settings.SECRET_KEY)
        print ("ALG = ", settings.ALGORITHM)
        claims = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return claims
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")