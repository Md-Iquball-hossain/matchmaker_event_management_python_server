import bcrypt
import jwt


def hash_password(password):
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying password: {str(e)}")
        return False

def create_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")

def verify_token(token, secret):
    try:
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
        print("JWt is valid. Decoded payload:", decoded_payload)
    except jwt.ExpiredSignatureError:
        print("JWT has expired")
    except jwt.DecodeError:
        print("JWT decoding error. Token is invalid")