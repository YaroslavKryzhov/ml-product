import logging
from enum import Enum
from typing import Any

from cent import Client

from ml_api.common import config

logger = logging.getLogger(__name__)


class Channel(Enum):
    PROJECT = {
        "prefix": "project",
        "subject": "info",
    }
    PIPELINE = {
        "prefix": "pipelines",
        "subject": "info",
    }
    INFO = {
        "prefix": "info",
        "subject": "info",
    }


class PubSub:
    channels: Channel = Channel

    def __init__(self, api_url: str, api_key: str) -> None:
        verify = config.STAGE != "local"
        self.client = Client(address=api_url, api_key=api_key, verify=verify)

    def _publish(
            self,
            prefix: str,
            channel_name: str,
            subject: str = "",
            message: Any = "",
            owner: str = "Services quimly",
    ) -> None:
        channel = f"{prefix}:{channel_name}"
        data = {"subject": subject, "message": message, "from": owner}
        try:
            return self.client.publish(channel, data)
        except Exception as e:
            logger.error(f"\nError when publishing at channel: {channel}: {e}\n")

    def publish_to_channel(
            self, channel: Channel, channel_name: str, message: Any
    ) -> None:
        self._publish(
            prefix=channel.value.get("prefix"),
            channel_name=channel_name,
            message=message,
            subject=channel.value.get("subject"),
        )
