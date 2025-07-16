"""Order API endpoint for creating an order and publishing to Kafka."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from order.app.db.session import get_session
from order.app.kafka.producer import kafka_producer
from order.app.models.orders import Order
from order.app.core.config import settings

router = APIRouter()
logger = logging.getLogger("order-api")
tracer = trace.get_tracer(__name__)


@router.post("/order")
async def create_order(order_data: Order, session: Session = Depends(get_session)):
    """
    Create a new order in the database and publish the event to Kafka.

    Args:
        order_data (OrderCreate): The order details from the request body.
        session (Session): SQLModel database session (injected).

    Returns:
        dict: Success message and created order ID.
    """
    with tracer.start_as_current_span("order.create") as span:
        try:
            # Persist order to DB
            order = Order(**order_data.model_dump())
            session.add(order)
            session.commit()
            session.refresh(order)

            # Add trace metadata
            span.set_attribute("order.id", order.id)
            span.set_attribute("order.item", order.item)
            span.set_attribute("order.quantity", order.quantity)

            logger.info(
                "Order created",
                extra={
                    "order_id": order.id,
                    "item": order.item,
                    "quantity": order.quantity,
                    "trace_id": trace.format_trace_id(span.get_span_context().trace_id),
                },
            )

            # Send to Kafka
            event = order.model_dump()
            await kafka_producer.send(settings.kafka_order_topic, event)

            logger.info(
                f"Event published to Kafka topic '{settings.kafka_order_topic}'",
                extra={"order_id": order.id},
            )

            return {"message": "Order placed successfully", "order_id": order.id}

        except SQLAlchemyError as db_err:
            logger.error("Database error during order creation", exc_info=True)
            span.set_status(Status(StatusCode.ERROR, str(db_err)))
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while creating order",
            )

        except Exception as kafka_err:
            logger.error("Failed to publish order event to Kafka", exc_info=True)
            span.set_status(Status(StatusCode.ERROR, str(kafka_err)))
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to publish order event",
            )
