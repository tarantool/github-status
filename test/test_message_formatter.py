import time

from watcher.incident_registry import Incident
from watcher.message_formatter import MessageFormatter


class TestMessageFormatter:

    def test_incident(self):
        incident = Incident(
            component="test_component",
            description="test_description",
            impact="test_impact",
            status="test_status",
            timestamp=time.time(),
            notified=False
        )
        expected = "🔴 New incident\n" \
                   "<b>Component:</b> test_component\n" \
                   "<b>Description:</b> test_description\n" \
                   "<b>Status:</b> test_status\n" \
                   "<b>Impact:</b> test_impact\n"

        assert MessageFormatter().incident(incident) == expected

    def test_all_resolved(self):
        expected = "🟢 All incidents resolved\n"
        assert MessageFormatter().all_resolved() == expected
