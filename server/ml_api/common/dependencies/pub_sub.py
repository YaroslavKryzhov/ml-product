import logging
from typing import Generator

from ml_api import config
from ml_api.common.pubsub.client import PubSub

logger = logging.getLogger(__name__)


def get_pubsub_client() -> Generator[None, None, PubSub]:
    """
    Dependency function that yields pubsub clients
    """
    yield PubSub(api_url=config.CENTRIFUGO_PUB_API, api_key=str(config.CENTRIFUDO_API_KEY))