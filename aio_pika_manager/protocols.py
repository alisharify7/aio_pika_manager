"""
* aiopika connection manager
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/aio_pika_manager
"""

from typing import Protocol, Dict

import aiologger
from aio_pika.abc import AbstractRobustQueue, AbstractRobustConnection


class RabbitMQConnectionBaseProtocol(Protocol):
    logger: aiologger.Logger
    queues: Dict[str, AbstractRobustQueue]
    channels: dict
    connection: AbstractRobustConnection
