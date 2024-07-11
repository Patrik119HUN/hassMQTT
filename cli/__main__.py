from core.mqtt import mqtt_manager
from core.home_assistant.mqtt_adapter import get_discovery
from core.home_assistant.device_observer import *
from core.mqtt.topic_builder import Topic, TopicType
from core.device_manager import device_manager
import json
import asyncio
from core.home_assistant.device_observer.observer_factory import *

observer_factory = ObserverFactory(mqtt_manager)


async def create_device(device):
    topic, discovery_packet = get_discovery(device)
    mqtt_manager.publish(topic, json.dumps(discovery_packet, indent=2))
    mqtt_manager.publish(Topic.from_str(TopicType.PUBLISHER, discovery_packet["availability_topic"]), "online")
    observers = observer_factory.get_observers(device, discovery_packet)
    for topic, observer in observers.items():
        subscribe_topic = Topic.from_str(TopicType.SUBSCRIBER, topic)
        mqtt_manager.add_subscriber(subscribe_topic, observer)


async def main():
    async with asyncio.TaskGroup() as tg:
        for device in device_manager.list():
            tg.create_task(create_device(device))


if __name__ == "__main__":
    asyncio.run(main())
    mqtt_manager.loop()
