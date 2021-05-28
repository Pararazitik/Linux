import asyncio
from idlelib.pyshell import HOST, PORT


async def tcpechoclient(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    message = 'Hello, world'

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    writer.close()
    await writer.wait_closed()


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode('sefsef')

    writer.write(data)
    await writer.drain()

    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()