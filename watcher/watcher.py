import time

from settings import Config
from watcher.githubclient import GithubClient
from watcher.incident_registry import IncidentRegistry, Incident
from watcher.message_formatter import MessageFormatter
from watcher.vkteams_bot import VKTeamsBot


def endless_loop_decorator(func, interval=Config().status_checking_interval):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            time.sleep(interval)

    return wrapper


class Watcher:

    def __init__(self, config: Config):
        self.config = config
        self.client = GithubClient(api_url=self.config.github_api_url)
        self.teamsbot = VKTeamsBot(token=self.config.bot_token,
                                   api_url=self.config.bot_api_url,
                                   chat_id=self.config.chat_id)
        self.incident_registry = IncidentRegistry()

    @endless_loop_decorator
    def run(self):
        status_info = self.client.get_status().json()
        if status_info["status"]["indicator"] != "none":
            unresolved = self.client.get_unresolved_incidents().json()
            if len(unresolved["incidents"]) >= 1:
                incident_list = unresolved["incidents"]
                component_name = incident_list[0]["components"][0]["name"]
                if self.incident_registry.get(component_name) is None:
                    self.incident_registry.add(
                        Incident(
                            component=component_name,
                            description=incident_list[0]["name"],
                            status=incident_list[0]["status"],
                            impact=incident_list[0]["impact"],
                            timestamp=time.time(),
                            notified=False
                        ))
        else:
            if self.incident_registry.list():
                self.teamsbot.send_message(message=MessageFormatter.all_resolved())
                self.incident_registry.clear()

        for incident in self.incident_registry.list():
            if not incident.notified:
                if (time.time() - incident.timestamp) >= self.config.notification_delay:
                    self.incident_registry.update(incident.component, "notified", True)
                    self.teamsbot.send_message(message=MessageFormatter.incident(incident))
