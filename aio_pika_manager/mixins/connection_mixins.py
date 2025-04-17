"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

import asyncio
from typing import Protocol, TypeVar

import aio_pika

from aio_pika_manager.protocols import RabbitMQConnectionBaseProtocol

T = TypeVar("T", bound="ConnectionProtocol")


class ConnectionProtocol(RabbitMQConnectionBaseProtocol, Protocol):
    pass


class ConnectionMixin:

    async def _connect(self: T) -> None:
        """
        Connects to RabbitMQ using the provided credentials and connection parameters.
        Retries the connection up to `max_retry_connection` times in case of failure.

        Raises:
            RuntimeError: If the maximum number of connection retries is exceeded.
        """
        self.logger.info(f"rabbitmq: trying to connect to {self.host}:{self.port}")
        retries = 0
        while retries <= self.max_retry_connection:
            try:
                self.connection = await aio_pika.connect_robust(
                    login=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    virtual_host=self.virtual_host,
                )
                self.logger.info(
                    f"rabbitmq: connected successfully to {self.host}:{self.port}"
                )
                return
            except aio_pika.exceptions.AMQPError as e:
                retries += 1
                wait_time = retries * 2
                self.logger.info(
                    f"rabbitmq: connection failed for {self.host}:{self.port}, retry number:{retries}, wait_for: {wait_time}s,\nreason: {e.reason}"
                )
                await asyncio.sleep(wait_time)

        self.logger.info(
            f"rabbitmq: connection failed for {self.host}:{self.port}, Connection error: Exceeded maximum number of connection retries"
        )

        raise RuntimeError(
            "Connection error: Exceeded maximum number of connection retries."
        )

    async def _close(self: T) -> None:
        """
        Closes the current connection if it is open.
        """
        if self.connection and not self.connection.is_closed:
            # close all channels <check if we close connection all channels will be closed automatically or not, just for now>
            for channel in self.channels:
                await self.channels[channel].close()
                await self.logger.info(f"connection to channel: {channel} closed.")

            await self.connection.close()
            await self.logger.info(
                f"rabbitmq: connection to {self.host}:{self.port} closed."
            )
            self.connection = None
