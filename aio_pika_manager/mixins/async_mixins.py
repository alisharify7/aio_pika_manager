"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

from typing import Protocol, TypeVar

T = TypeVar("T", bound="ConnectionProtocol")


class ConnectionProtocol(Protocol):
    async def _connect(self) -> None: ...

    async def _close(self) -> None: ...


class AsyncMixin:
    """
    Requires:
        - self._connect(): Coroutine to establish a connection.
        - self._close(): Coroutine to close the connection.
    """

    async def __aenter__(self: T) -> T:
        """
        Asynchronous context manager entry method. Ensures the connection is established.

        Returns:
            RabbitMQManger: The current instance of the manager.
        """
        if self.connection and not self.connection.is_closed:
            return self
        await self._connect()
        return self

    async def __aexit__(self: T, exc_type, exc_val, exc_tb) -> None:
        """
        Asynchronous context manager exit method. Closes the connection when exiting the context.

        Args:
            exc_type: The exception type (if any).
            exc_val: The exception value (if any).
            exc_tb: The traceback (if any).
        """
        await self._close()
