from typing import Any, Dict, Generic, Optional, Type, TypeVar

import bson.errors
from bunnet import PydanticObjectId
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.models import ID, OAP
from fastapi_users.exceptions import InvalidID

from ml_api.apps.users.model import BunnetBaseUserDocument


UP_BUNNET = TypeVar("UP_BUNNET", bound=BunnetBaseUserDocument)


class BunnetUserDatabase(
    Generic[UP_BUNNET], BaseUserDatabase[UP_BUNNET, PydanticObjectId]
):
    """
    Database adapter for Bunnet.

    :param user_model: Beanie user model.
    :param oauth_account_model: Optional Beanie OAuth account model.
    """

    def __init__(
        self,
        user_model: Type[UP_BUNNET],
    ):
        self.user_model = user_model
        self.oauth_account_model = None

    async def get(self, id: ID) -> Optional[UP_BUNNET]:
        """Get a single user by id."""
        return self.user_model.get(id).run()  # type: ignore

    async def get_by_email(self, email: str) -> Optional[UP_BUNNET]:
        """Get a single user by email."""
        return self.user_model.find_one(
            self.user_model.email == email,
            collation=self.user_model.Settings.email_collation,
        ).run()

    async def get_by_oauth_account(
        self, oauth: str, account_id: str
    ) -> Optional[UP_BUNNET]:
        """Get a single user by OAuth account id."""
        # if self.oauth_account_model is None:
        raise NotImplementedError()
        #
        # return self.user_model.find_one(
        #     {
        #         "oauth_accounts.oauth_name": oauth,
        #         "oauth_accounts.account_id": account_id,
        #     }
        # ).run()

    async def create(self, create_dict: Dict[str, Any]) -> UP_BUNNET:
        """Create a user."""
        user = self.user_model(**create_dict)
        user.create()
        return user

    async def update(self, user: UP_BUNNET, update_dict: Dict[str, Any]) -> UP_BUNNET:
        """Update a user."""
        for key, value in update_dict.items():
            setattr(user, key, value)
        user.save()
        return user

    async def delete(self, user: UP_BUNNET) -> None:
        """Delete a user."""
        user.delete()

    async def add_oauth_account(
        self, user: UP_BUNNET, create_dict: Dict[str, Any]
    ) -> UP_BUNNET:
        # """Create an OAuth account and add it to the user."""
        # if self.oauth_account_model is None:
        raise NotImplementedError()
        #
        # oauth_account = self.oauth_account_model(**create_dict)
        # user.oauth_accounts.append(oauth_account)  # type: ignore
        #
        # user.save()
        # return user

    async def update_oauth_account(
        self, user: UP_BUNNET, oauth_account: OAP, update_dict: Dict[str, Any]
    ) -> UP_BUNNET:
        # """Update an OAuth account on a user."""
        # if self.oauth_account_model is None:
        raise NotImplementedError()
        #
        # for i, existing_oauth_account in enumerate(user.oauth_accounts):  # type: ignore
        #     if (
        #         existing_oauth_account.oauth_name == oauth_account.oauth_name
        #         and existing_oauth_account.account_id == oauth_account.account_id
        #     ):
        #         for key, value in update_dict.items():
        #             setattr(user.oauth_accounts[i], key, value)  # type: ignore
        #
        # user.save()
        # return user


class ObjectIDIDMixin:
    def parse_id(self, value: Any) -> PydanticObjectId:
        try:
            return PydanticObjectId(value)
        except (bson.errors.InvalidId, TypeError) as e:
            raise InvalidID() from e