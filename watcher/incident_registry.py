from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Incident:
    component: str
    description: str
    impact: str
    status: str
    timestamp: float
    notified: bool


class IncidentRegistry:

    def __init__(self):
        self.registry = []

    def add(self, incident: Incident):
        self.registry.append(incident)

    def delete(self, incident: Incident):
        raise NotImplementedError

    def list(self) -> list:
        return self.registry

    def clear(self):
        self.registry.clear()

    def get(self, component_name: str) -> Optional[Incident]:
        for incident in self.registry:
            if incident.component == component_name:
                return incident
        return None

    def update(self, component_name: str, field: str, value: Optional[Any]):
        for incident in self.registry:
            if incident.component == component_name:
                if incident.__dict__.get(field) is None:
                    raise ValueError(f"Field with name {field} not found.")
                incident.__dict__[field] = value
                return
        raise NameError(f"Component with name {component_name} not found.")
