"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

from typing import TypeVar, Protocol

from aio_pika.abc import AbstractRobustChannel
from tabulate import tabulate

from aio_pika_manager.protocols import RabbitMQConnectionBaseProtocol

T = TypeVar("T", bound="StatusProtocol")


class StatusProtocol(RabbitMQConnectionBaseProtocol, Protocol):
    async def get_channel(self, channel_name: str) -> AbstractRobustChannel: ...


class StatusMixin:

    async def status_channels(self: T) -> None:
        """
            print status of all channels in table format
        :return: None
        """

        table_data = []
        for channel in self.channels:
            table_data.append(
                (
                    channel,
                    (
                        "Connected"
                        if not self.channels[channel].is_closed
                        else "Disconnected"
                    ),
                )
            )
        print()
        print(
            tabulate(table_data, ["channel name", "channel status"], tablefmt="github")
        )
        print()
