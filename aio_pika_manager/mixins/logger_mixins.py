"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

import logging
from typing import Protocol, TypeVar

from aio_pika_manager.protocols import RabbitMQConnectionBaseProtocol
from aio_pika_manager.utils.logger import get_async_logger

T = TypeVar("T", bound="LoggerProtocol")


class LoggerProtocol(RabbitMQConnectionBaseProtocol, Protocol):
    pass


class LoggerMixin:

    async def setup_logger(
        self, logger_name: str = "aio_pika_manager", log_file: str | None = None
    ):
        """
        setup logger for main Connection manager class.
        add logger property to current instance.
        Args:
            logger_name:
            log_file:

        Returns:

        """
        self.logger = await get_async_logger(
            log_level=logging.INFO,
            log_file=log_file,
            logger_name=logger_name,
        )
        await self.logger.info("Logger Created successfully.")
