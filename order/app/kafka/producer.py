"""Kafka producer wrapper for sending JSON-encoded messages asynchronously."""

import json
import logging
from aiokafka import AIOKafkaProducer

from order.app.core.config import settings
from opentelemetry import trace


tracer = trace.get_tracer(__name__)
logger = logging.getLogger("kafka-producer")


class KafkaProducerWrapper:
    """A wrapper around AIOKafkaProducer with JSON serialization."""

    def __init__(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=self._json_serializer,
        )

    def _json_serializer(self, value: dict) -> bytes:
        """
        Serialize a Python dictionary into a JSON-encoded UTF-8 byte string.
        """
        return json.dumps(value).encode("utf-8")

    async def start(self) -> None:
        """Start the Kafka producer."""
        logger.info("Starting Kafka producer...")
        await self.producer.start()

    async def stop(self) -> None:
        """Stop the Kafka producer."""
        logger.info("Stopping Kafka producer...")
        await self.producer.stop()

    async def send(self, topic: str, message: dict) -> None:
        """
        Send a message to the given Kafka topic.

        Args:
            topic (str): The Kafka topic name.
            message (dict): The message payload.
        """
        with tracer.start_as_current_span("kafka.produce") as span:
            span.set_attribute("messaging.system", "kafka")
            span.set_attribute("messaging.destination", topic)
            span.set_attribute("messaging.destination_kind", "topic")
            span.set_attribute("messaging.kafka.message", str(message))

            logger.info(f"Sending message to topic '{topic}': {message}")
            await self.producer.send_and_wait(topic, message)


# Singleton instance
kafka_producer = KafkaProducerWrapper()
