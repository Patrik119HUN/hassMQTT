from dataclasses import dataclass
from typing import Dict
from core.home_assistant.device_observer.entity_observer import EntityObserver


@dataclass
class ObserverData:
    command_observer: EntityObserver
    state_observer: EntityObserver
    other_observers: Dict[str, EntityObserver]
