import aiohttp
from nicegui import ui

class RegisterScreen(ui.Block):
    def __init__(self, api_url):
        self.api_url = api_url
        self.username_input = ui.textbox('Username:')
        self.password_input = ui.password('Password:')
        self.email_input = ui.textbox('Email:')
        self.register_button = ui.button('Register', on_click=self.register)

        super().__init__(
            ui.label('Register'),
            self.username_input,
            self.password_input,
            self.email_input,
            self.register_button
        )

    async def register(self):
        username = self.username_input.get_value()
        password = self.password_input.get_value()
        email = self.email_input.get_value()

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.api_url}/api/users/signup', json={'username': username, 'password': password, 'email': email}) as response:
                if response.status == 201:
                    # Successfully registered, handle the response accordingly
                    print(f'Registration successful for user: {username}')
                else:
                    # Handle registration failure
                    print('Registration failed')

# Usage in main.py:
# register_screen = RegisterScreen(api_url='http://localhost:5000')
