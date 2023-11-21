import logging

from cent import Client

from ml_api import config
from ml_api.apps.jobs.model import BackgroundJob

logger = logging.getLogger(__name__)


class PubSub:
    def __init__(self, api_url: str, api_key: str) -> None:
        self.client = Client(address=api_url, api_key=api_key)
        self.channel_name: str = "INFO"

    def _publish(self, channel_name: str, user_id: str, job_type: str,
                 object_id: str, status: str, message: str) -> None:
        channel = f"{channel_name}#{user_id}"
        logger.error(channel)
        data = {
            "job_type": job_type,
            "object_id": object_id,
            "status": status,
            "message": message
        }
        try:
            print(channel, data)
            return self.client.publish(channel, data)
        except Exception as e:
            logger.error(f"\nError when publishing at channel: {channel}: {e}\n")

    def publish_to_channel(self, job_info: BackgroundJob) -> None:
        self._publish(
            channel_name=self.channel_name,
            user_id=str(job_info.user_id),
            job_type=job_info.type.value,
            object_id=str(job_info.object_id),
            status=job_info.status.value,
            message=job_info.output_message,
        )


def get_pubsub_client() -> PubSub:
    return PubSub(
        api_url=config.CENTRIFUGO_PUB_API,
        api_key=config.CENTRIFUDO_API_KEY
    )
