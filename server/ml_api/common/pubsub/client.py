import logging
from enum import Enum
from typing import Any

from cent import Client

from ml_api import config

logger = logging.getLogger(__name__)


class PubSub:

    def __init__(self, api_url: str, api_key: str) -> None:
        verify = config.STAGE != "local"
        self.client = Client(address=api_url, api_key=api_key, verify=verify)

    def _publish(
            self,
            channel_name: str,
            message: Any = "",
    ) -> None:
        channel = f"{channel_name}"
        data = {"message": message}
        try:
            return self.client.publish(channel, data)
        except Exception as e:
            logger.error(f"\nError when publishing at channel: {channel}: {e}\n")

    def publish_to_channel(
            self, message: Any,  channel_name: str = "INFO") -> None:
        self._publish(
            channel_name=channel_name,
            message=message,
        )
