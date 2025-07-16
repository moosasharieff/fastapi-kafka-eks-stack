"""App configuration settings using Pydantic BaseSettings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-specific configuration loaded from .env or environment."""

    kafka_bootstrap_servers: str = Field(
        ...,
        env="KAFKA_BOOTSTRAP_SERVERS",
        description="Kafka broker list (comma-separated)",
    )
    kafka_order_topic: str = Field(
        default="orders.created", description="Kafka topic name for order events"
    )
    postgres_dsn: str = Field(
        ..., env="POSTGRES_DSN", description="PostgreSQL connection string"
    )
    service_name: str = Field(
        default="order-service", description="Name of the microservice"
    )

    model_config = SettingsConfigDict(env_file=".env")


# Instantiate settings
settings = Settings()
