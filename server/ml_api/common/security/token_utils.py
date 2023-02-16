import jwt

from ml_api import config


def create_centrifugo_token(*, user_id: str):
    to_encode = {"sub": user_id}
    # expire = datetime.utcnow() + timedelta(minutes=15)
    # to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode,
                             str(config.CENTRIFUGO_HMAC),
                             algorithm="HS256")
    return encoded_jwt
