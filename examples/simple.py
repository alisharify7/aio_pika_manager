import asyncio
from aio_pika_manager import RabbitMQManger
from aio_pika_manager.aiopika import Message


async def main():
    # manager = RabbitMQManger(
    #     username="guest",
    #     password="guest",
    #     host="localhost",
    #     port=5672,
    #     virtual_host="/",
    #     max_retry_connection=30,
    # )
    # await manager.setup_logger() # this should be called for setting up logger

    # or just call create method

    manager = await RabbitMQManger.create(
        username="guest",
        password="guest",
        host="localhost",
        port=5672,
        virtual_host="/",
        max_retry_connection=30,
    )

    async with manager as rabbit_manager:
        queue_name = "test_queue"
        channel_name = "test_channel"
        channel = await rabbit_manager.get_channel(channel_name=channel_name)
        await channel.default_exchange.publish(
            message=Message(body="test_message".encode()),
            routing_key=queue_name,
        )
        print("message published successfully.")
        await rabbit_manager.status_channels()
        await rabbit_manager.status_queues()


if __name__ == "__main__":
    asyncio.run(main())
