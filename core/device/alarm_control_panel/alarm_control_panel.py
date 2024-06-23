from core.device.entity import Entity
from core.device.hardware import Hardware


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

    def state(self):
        self.driver.get_data(1, 0)

    def arm_home(self):
        self.driver.send_data(0, 1)

    def arm_away(self):
        self.driver.send_data(0, 2)

    def arm_night(self):
        self.driver.send_data(0, 3)

    def arm_vacation(self):
        self.driver.send_data(0, 4)

    def arm_custom(self):
        self.driver.send_data(0, 5)