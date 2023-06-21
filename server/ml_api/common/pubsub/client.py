import logging
from typing import Any, Generator

from cent import Client

from ml_api import config

logger = logging.getLogger(__name__)


class PubSub:

    def __init__(self, api_url: str, api_key: str) -> None:
        self.client = Client(address=api_url, api_key=api_key)

    def _publish(
            self,
            channel_name: str,
            user_id: str,
            task_id: str,
            status: str,
            message: str = "",
    ) -> None:
        channel = f"{channel_name}#{user_id}"
        logger.error(channel)
        data = {"task_id": task_id, "status": status, "message": message}
        try:
            return self.client.publish(channel, data)
        except Exception as e:
            logger.error(f"\nError when publishing at channel: {channel}: {e}\n")

    def publish_to_channel(
            self, user_id: str, task_id: str,
            status: str, message: Any,  channel_name: str = "INFO") -> None:
        self._publish(
            channel_name=channel_name,
            user_id=user_id,
            task_id=task_id, status=status,
            message=str(message),
        )


def get_pubsub_client() -> Generator[None, None, PubSub]:
    """
    Dependency function that yields pubsub client
    """
    yield PubSub(api_url=config.CENTRIFUGO_PUB_API, api_key=str(config.CENTRIFUDO_API_KEY))