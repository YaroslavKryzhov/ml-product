import logging
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
# import jwt
# from sqlalchemy.orm import Session
#
# from wt.common import config
# from wt.apps.users.models import User
# from wt.apps.users.repository import CRUDUser
# from wt.common.dependencies import db_deps
# from wt.common.exceptions import wt_exceptions

# logger = logging.getLogger(__name__)
#
# google_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.AUTH_TOKEN_GOOGLE_URL)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.AUTH_TOKEN__PASSWD_URL)


def get_current_user(
        # google_token: str = Depends(google_oauth2_scheme),
        # bearer_token: str = Depends(oauth2_scheme),
        # db: Session = Depends(db_deps.get_db)
):
    # token = bearer_token or google_token
    # try:
    #     payload = jwt.decode(token,
    #                          str(config.SECRET_KEY),
    #                          algorithms=[config.API_ALGORITHM])
    #     email: str = payload.get('sub')
    #     name: str = payload.get('name')
    #     picture: str = payload.get('picture')
    #     if email is None:
    #         raise wt_exceptions.CREDENTIALS_EXCEPTION
    # except jwt.PyJWTError as e:
    #     logger.error(e)
    #     raise wt_exceptions.CREDENTIALS_EXCEPTION
    #
    # user = CRUDUser(User)
    # if user.get_by_email(db, email=email):
    #     return {
    #         'name': name,
    #         'email': email,
    #         'picture': picture
    #     }
    # logger.warning(f'User "{email}" does not in db!')
    # raise wt_exceptions.CREDENTIALS_EXCEPTION
    return 'admin'
