from watcher.incident_registry import Incident


class MessageFormatter:
    @staticmethod
    def incident(incident: Incident) -> str:
        return "🔴 New incident\n" \
               f"<b>Component:</b> {incident.component}\n" \
               f"<b>Description:</b> {incident.description}\n" \
               f"<b>Status:</b> {incident.status}\n" \
               f"<b>Impact:</b> {incident.impact}\n"

    @staticmethod
    def incident_resolved(incident: Incident):
        return "🟢 Incident resolved\n" \
               f"<b>Component:</b> {incident.component}\n"

    @staticmethod
    def all_resolved() -> str:
        return "🟢 All incidents resolved\n"
