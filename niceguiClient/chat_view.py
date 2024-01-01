import aiohttp
from nicegui import ui

class ChatViewScreen():
    def __init__(self, api_url):
        self.api_url = api_url
        self.room_messages = ui.list([], height=300)
        self.message_input = i = ui.textarea(value='Type your message:').props('clearable')
        self.send_message_button = ui.button('Send Message', on_click=self.send_message)

        super().__init__(
            ui.label('Chat View'),
            self.room_messages,
            self.message_input,
            self.send_message_button
        )

        # Additional variables to keep track of the selected room and username
        self.selected_room = None
        self.username = None

    async def send_message(self):
        message = self.message_input.get_value()

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.api_url}/api/rooms/{self.selected_room}/messages', json={'user': self.username, 'message': message}) as response:
                if response.status == 200:
                    print(f'Message sent successfully: {message}')
                    # Update the displayed messages
                    await self.fetch_messages()
                else:
                    print('Failed to send message')

    async def fetch_messages(self):
        if not self.selected_room:
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/api/rooms/{self.selected_room}/messages') as response:
                if response.status == 200:
                    messages = await response.json()
                    self.room_messages.set(messages)
                else:
                    print('Failed to fetch messages')

    # Additional methods to update the displayed messages based on the selected room
    async def select_room(self, room_name):
        self.selected_room = room_name
        await self.fetch_messages()
        print(f'Selected room: {room_name}')

# Usage in main.py:
# chat_view_screen = ChatViewScreen(api_url='http://localhost:5000')
# chat_view_screen.username = 'Alice'  # Set the username
# chat_view_screen.selected_room = 'room1'  # Set the initial selected room
# chat_view_screen.fetch_messages()  # Fetch and display messages for the initial room
