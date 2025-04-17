"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

from typing import Protocol, TypeVar

from aio_pika.abc import AbstractRobustChannel

from aio_pika_manager.protocols import RabbitMQConnectionBaseProtocol

T = TypeVar("T", bound="ChannelProtocol")


class ChannelProtocol(RabbitMQConnectionBaseProtocol, Protocol):
    async def get_channel(self, channel_name: str) -> AbstractRobustChannel: ...


class ChannelMixin:

    async def get_channel(self: T, channel_name: str) -> AbstractRobustChannel:
        """
        Returns an active RabbitMQ channel. If no active channel exists, creates one.

        Returns:
            AbstractRobustChannel: The active RabbitMQ channel.
        """
        if self.connection is None or self.connection.is_closed:
            await self._connect()

        if channel_name not in self.channels:
            self.channels[channel_name] = await self.connection.channel()
        elif self.channels[channel_name].is_closed:
            self.channels.pop(channel_name)
            self.channels[channel_name] = await self.connection.channel()

        return self.channels[channel_name]
