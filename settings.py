import os
from dataclasses import dataclass


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
@dataclass
class Config:
    chat_id: str
    bot_token: str
    retry_request_delay: int
    status_checking_interval: int
    notification_delay: int
    bot_api_url: str
    github_api_url: str

    def __init__(self):
        self.retry_request_delay = int(os.environ.get("RETRY_REQUEST_DELAY", "5"))
        self.status_checking_interval = int(os.environ.get("STATUS_CHECKING_INTERVAL", "30"))
        self.notification_delay = int(os.environ.get("NOTIFICATION_DELAY", "120"))
        self.bot_api_url = os.environ.get("BOT_API_URL", "https://api.internal.myteam.mail.ru/bot/v1")
        self.github_api_url = os.environ.get("GITHUB_API_URL", "https://www.githubstatus.com/api/v2")

    def load_required(self):
        _chat_id = os.environ.get("CHAT_ID")
        assert _chat_id, "Environment variable CHAT_ID not set."
        self.chat_id = _chat_id

        _bot_token = os.environ.get("BOT_TOKEN")
        assert _bot_token, "Environment variable BOT_TOKEN not set."
        self.bot_token = _bot_token
