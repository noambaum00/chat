import aiohttp
from nicegui import ui
from '/home/noampc2jesica/.local/lib/python3.12/site-packages/nicegui/context.py' import container_element
class LoginScreen():
    def __init__(self, api_url):
        self.api_url = api_url
        self.username_input = ui.input(label = 'Username:', placeholder='start typing',)
        self.password_input = ui.password('Password:')
        self.login_button = ui.button('Login', on_click=self.login)

        super().__init__(
            ui.label('Login'),
            self.username_input,
            self.password_input,
            self.login_button
        )

    async def login(self):
        username = self.username_input.get_value()
        password = self.password_input.get_value()
        #add valeu chack
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.api_url}/api/users/login', json={'username': username, 'password': password}) as response:
                if response.status == 200:
                    # Successfully logged in, handle the response accordingly
                    print(f'Login successful for user: {username}')
                else:
                    # Handle login failure
                    print('Login failed')

# Usage in main.py:
# login_screen = LoginScreen(api_url='http://localhost:5000')
