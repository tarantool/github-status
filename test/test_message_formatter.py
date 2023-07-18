import time

from watcher.incident_registry import Incident
from watcher.message_formatter import MessageFormatter


class TestMessageFormatter:

    def test_incident(self):
        incident = Incident(
            components=["test_component", "test_component2"],
            description="test_description",
            impact="test_impact",
            status="test_status",
            site_url="test_site",
            timestamp=time.time(),
            notified=False
        )
        expected = "🔴 New incident\n" \
                   "<b>Components:</b> test_component, test_component2\n" \
                   "<b>Description:</b> test_description\n" \
                   "<b>Status:</b> test_status\n" \
                   "<b>Impact:</b> test_impact\n" \
                   "<b>URL:</b> test_site\n"

        assert MessageFormatter().incident(incident) == expected

    def test_all_resolved(self):
        expected = "🟢 All incidents resolved\n"
        assert MessageFormatter().all_resolved() == expected
