import aiohttp
from nicegui import ui

class ChatSelectionScreen():
    def __init__(self, api_url):
        self.api_url = api_url
        self.get_rooms_button = ui.button('Get Rooms', on_click=self.get_rooms)
        self.room_list = ui.list([], height=200)
        self.join_room_input = ui.textbox('Enter Room Name:')
        self.join_room_button = ui.button('Join Room', on_click=self.join_room)

        super().__init__(
            ui.label('Chat Selection'),
            self.get_rooms_button,
            self.room_list,
            self.join_room_input,
            self.join_room_button
        )

    async def get_rooms(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/api/rooms') as response:
                if response.status == 200:
                    rooms = await response.json()
                    self.room_list.set(rooms)
                else:
                    print('Failed to fetch rooms')

    async def join_room(self):
        room_name = self.join_room_input.get_value()

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.api_url}/api/users/{self.username}/join_room', json={'room_name': room_name}) as response:
                if response.status == 200:
                    print(f'Successfully joined room: {room_name}')
                else:
                    print(f'Failed to join room: {room_name}')

# Usage in main.py:
# chat_selection_screen = ChatSelectionScreen(api_url='http://localhost:5000')
