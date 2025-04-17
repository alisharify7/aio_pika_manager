"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""
from typing import Protocol, TypeVar

from aio_pika.abc import AbstractRobustQueue, AbstractRobustChannel

from aio_pika_manager.protocols import RabbitMQConnectionBaseProtocol

T = TypeVar("T", bound="QueueProtocol")


class QueueProtocol(RabbitMQConnectionBaseProtocol, Protocol):
    async def get_channel(self, channel_name: str) -> AbstractRobustChannel: ...


class QueueMixin:
    async def declare_queue(
            self: T, queue_name: str, channel_name: str, *args, **kwargs
    ) -> AbstractRobustQueue:
        """
        Declares a queue in RabbitMQ if not already declared, otherwise returns the existing queue.

        Args:
            queue_name (str): The name of the queue to declare.

        Returns:
            AbstractRobustQueue: The declared or existing queue.
        """
        if queue_name in self.queues:
            await self.logger.info(
                f"rabbitmq: Queue '{queue_name}' already declared, returning existing one."
            )
            return self.queues[queue_name]

        channel = await self.get_channel(channel_name=channel_name)

        queue = await channel.declare_queue(queue_name, *args, **kwargs)
        self.queues[queue_name] = queue  # Store the declared queue
        await self.logger.info(f"rabbitmq: Queue '{queue_name}' declared successfully.")
        return queue
