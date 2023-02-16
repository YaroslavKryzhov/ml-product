import logging
from typing import Any

from cent import Client

logger = logging.getLogger(__name__)


class PubSub:

    def __init__(self, api_url: str, api_key: str) -> None:
        self.client = Client(address=api_url, api_key=api_key)

    def _publish(
            self,
            channel_name: str,
            task_id: str,
            status: str,
            message: str = "",
    ) -> None:
        channel = f"{channel_name}"
        data = {"task_id": task_id, "status": status, "message": message}
        try:
            return self.client.publish(channel, data)
        except Exception as e:
            logger.error(f"\nError when publishing at channel: {channel}: {e}\n")

    def publish_to_channel(
            self, task_id: str,
            status: str, message: Any,  channel_name: str = "INFO") -> None:
        self._publish(
            channel_name=channel_name,
            task_id=task_id, status=status,
            message=message,
        )
