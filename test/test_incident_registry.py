import time

from watcher.incident_registry import IncidentRegistry, Incident


def get_incident() -> Incident:
    return Incident(
        components=["test_component", "test_component2"],
        description="test_description",
        impact="test_impact",
        status="test_status",
        site_url="test_site",
        timestamp=time.time(),
        notified=False
    )


class TestIncidentRegistry:

    def test_add(self):
        incident = get_incident()
        ir = IncidentRegistry()
        ir.add(incident)
        assert ir.list()[0] is incident

    def test_list(self):
        incident = get_incident()
        ir = IncidentRegistry()
        ir.add(incident)
        ir.add(incident)
        assert len(ir.list()) == 2
        assert ir.list()[0] is incident

    def test_clear(self):
        incident = get_incident()
        ir = IncidentRegistry()
        ir.add(incident)
        assert len(ir.list()) == 1

        ir.clear()
        assert len(ir.list()) == 0
