import hashlib
import os
import base64
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000 
    )
    return base64.b64encode(salt + key).decode('ascii')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        decoded = base64.b64decode(hashed_password)
        salt = decoded[:32]
        stored_key = decoded[32:]
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt,
            100000
        )
        return key == stored_key
    except:
        return False

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-dev-key-change-me")

def create_token(username: str) -> str:
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("username")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None