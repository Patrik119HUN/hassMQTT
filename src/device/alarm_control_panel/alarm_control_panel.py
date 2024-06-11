from src.device.entity import Entity
from src.device.hardware import Hardware


class AlarmControlPanel(Entity):

    def __init__(
        self,
        name: str,
        hardware: Hardware = None,
        icon: str = None,
        unique_id: str = None,
        entity_type: str = "alarm_control_panel",
    ):
        Entity.__init__(
            self,
            name=name,
            unique_id=unique_id,
            hardware=hardware,
            entity_type=entity_type,
            icon=icon,
        )

    def alarm(self):
        print("alarm")

    def disarm(self):
        print("disarm")

    def accept(self, visitor):
        visitor.alarm_control_panel(self)
