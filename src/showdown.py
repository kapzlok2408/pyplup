import websockets
from .constants import WEBSOCKET_URL

class Showdown:
    def __init__(self, username = '', password = ''):
        self.url = WEBSOCKET_URL
        self.username = username
        self.password = password
        self.battles = {}

    async def run(self):
        async for messages in self.connection:
            await self.process_messages(messages)

    from ._showdown_process import process_messages

    #send a message to the given room
    async def send_message(self, roomid, message):
        if roomid == "global":
            response = f"|{message}"
        else:
            response = f"{roomid}|{message}"
        await self.connection.send(response)

    # opens a connection
    async def connect(self):
        self.connection = await websockets.connect(self.url)

    # closes the existing connection
    async def close(self):
        if self.open:
            await self.connection.close()
