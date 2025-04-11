# AioPika

**AioPika** is an asynchronous RabbitMQ connection manager and queue handler built on top of the `aio_pika` library for efficient and scalable message processing in Python. It simplifies managing connections, channels, and queues in a RabbitMQ environment using asynchronous programming.

## Features

- Singleton-based connection manager to ensure a single connection to RabbitMQ.
- Support for declaring and reusing queues to avoid redundancy.
- Automatic connection retries with backoff in case of connection issues.
- Context manager support for clean resource management.
- Easy-to-use methods for producing and consuming messages.

## Installation

To install `AioPika`, you can use `pip`:

```bash
pip install aio_pika_manager
```

## Example Usage
Initialize the Manager
You can use AioPika as a context manager to handle the connection and channel automatically.

```python
import asyncio
from aio_pika import Message, DeliveryMode
from aio_pika_manager import RabbitMQManger

async def main():
    async with RabbitMQManger() as manager:
        channel = await manager.get_channel()
        # Declare a queue
        queue = await manager.declare_queue("my_queue")
        
        # Produce a message
        await channel.default_exchange.publish(
            Message(body="Hello, World!".encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue.name
        )
        print("Message sent!")
        
        # Consume a message
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                print(f"Received message: {message.body.decode()}")
                await message.ack()
                break

# Run the example
asyncio.run(main())
```

## Connection Management
The connection to RabbitMQ is established automatically when you use the context manager async with RabbitMQManger() as manager. You don't need to worry about closing the connection explicitly; it will be closed automatically when the context manager exits.

Declaring Queues
Queues are declared lazily, meaning the first time you try to access a queue, it will be declared. Afterward, the declared queue is cached and reused in subsequent operations.
```python
queue = await manager.declare_queue("my_queue")
```
## Producing Messages
To send a message, use the channel.default_exchange.publish method. Here’s an example of publishing a message to a queue:

```python
await channel.default_exchange.publish(
    Message(body="Hello, World!".encode(), delivery_mode=DeliveryMode.PERSISTENT),
    routing_key=queue.name
)
```
## Consuming Messages
To consume messages, you can iterate over the queue:

```python
async with queue.iterator() as queue_iter:
    async for message in queue_iter:
        print(f"Received message: {message.body.decode()}")
        await message.ack()
        break  # Stop after consuming one message (remove if you want to consume continuously)
```
## Methods

### `declare_queue(queue_name: str)`
Declares a queue with the given `queue_name`. If the queue already exists, it returns the existing one.

- **Arguments**: 
  - `queue_name` (str): The name of the queue to declare.
- **Returns**: The declared queue.

### `get_channel()`
Returns an active channel from the RabbitMQ connection. If the connection is closed or not established, it will reconnect automatically.

- **Returns**: An `AbstractRobustChannel`.

### `__aenter__()` and `__aexit__()`
These are the context manager methods used when wrapping the manager in an `async with` block. They ensure that connections are properly opened and closed.
