"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

import typing

from aio_pika.abc import AbstractRobustChannel
from aio_pika.robust_connection import AbstractRobustConnection
from aio_pika.robust_queue import AbstractRobustQueue

from aio_pika_manager.mixins import (
    LoggerMixin,
    StatusMixin,
    ChannelMixin,
    AsyncMixin,
    QueueMixin,
    ConnectionMixin,
)


class UpperManagerMixin(
    LoggerMixin, StatusMixin, ChannelMixin, AsyncMixin, QueueMixin, ConnectionMixin
):
    pass


class RabbitMQManger(UpperManagerMixin):
    """
    Manages the connection to RabbitMQ and allows the creation of channels and queues.
    This class follows the Singleton design pattern to ensure that only one instance exists.
    """

    # "Mixin with expected interface"
    # "Duck typing mixin"

    instance: typing.Optional["RabbitMQManger"] = None
    queues: typing.Dict[str, AbstractRobustQueue] = {}
    channels: typing.Dict[str, AbstractRobustChannel] = {}

    def __new__(cls, *args, **kwargs) -> "RabbitMQManger":
        """
        Singleton pattern to ensure only one instance of RabbitMQManger is created.

        Returns:
            RabbitMQManger: The singleton instance.
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        max_retry_connection: int = 10,
        virtual_host: str = "/",
        logger_name: str = "aio_pika_manager",
        log_file: str | None = None,
    ) -> None:
        """
        Initializes the RabbitMQManger instance.

        Args:
            host (str): The RabbitMQ server hostname (default: "localhost").
            port (int): The RabbitMQ server port (default: 5672).
            username (str): RabbitMQ username (default: "guest").
            password (str): RabbitMQ password (default: "guest").
            max_retry_connection (int): The maximum number of retry attempts for connecting to RabbitMQ (default: 10).
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection: typing.Optional[AbstractRobustConnection] = None
        self.max_retry_connection = max_retry_connection
        self.virtual_host = virtual_host

    @classmethod
    async def create(
        cls,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        max_retry_connection: int = 10,
        virtual_host: str = "/",
        logger_name: str = "aio_pika_manager",
        log_file: str | None = None,
    ) -> "RabbitMQManger":
        instance = cls(
            host=host,
            port=port,
            username=username,
            password=password,
            max_retry_connection=max_retry_connection,
            virtual_host=virtual_host,
            logger_name=logger_name,
            log_file=log_file,
        )
        await instance.setup_logger(logger_name=logger_name, log_file=log_file)
        return instance
