from core.mqtt import mqtt_manager, MQTTManager
from core.home_assistant.mqtt_packet import get_discovery
from core.home_assistant.device_observer import *
from core.mqtt.topic import Topic, TopicType
from core.device_manager import device_manager
import json
import asyncio
from core.home_assistant.device_observer import *
from loguru import logger
from core.device.entity import Entity


async def create_device(device: Entity):
    topic, discovery_packet = get_discovery(device)
    observer_factory.set_mqtt_manager(mqtt_manager)
    mqtt_manager.publish(topic, json.dumps(discovery_packet, indent=2))
    mqtt_manager.publish(
        Topic.from_str(TopicType.PUBLISHER, discovery_packet["availability_topic"]),
        "online",
    )
    observers = observer_factory.get_observers(device, discovery_packet)
    for topic, observer in observers.items():
        mqtt_manager.add_subscriber(topic, observer)
    logger.debug(f"created an {device.__class__.__name__}")


async def main():
    async with asyncio.TaskGroup() as tg:
        for device in device_manager.list():
            tg.create_task(create_device(device))


if __name__ == "__main__":
    asyncio.run(main())
    MQTTManager.instance().loop_forever()
