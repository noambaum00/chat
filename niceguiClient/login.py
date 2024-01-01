<<<<<<< HEAD
import aiohttp
from nicegui import ui
from '/home/noampc2jesica/.local/lib/python3.12/site-packages/nicegui/context.py' import container_element
class LoginScreen():
    def __init__(self, api_url):
        self.api_url = api_url
        self.username_input = ui.input(label = 'Username:', placeholder='start typing',)
        self.password_input = ui.password('Password:')
        self.login_button = ui.button('Login', on_click=self.login)
=======
from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import Client, app, ui
from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    email: EmailStr
>>>>>>> parent of 0abc1cc (renew gui.)


<<<<<<< HEAD
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
=======

@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:
        username_value = username.value
        password_value = password.value

        # Client-side validation
        if not (any(char.isdigit() for char in password_value) and any(char.isalpha() for char in password_value) and len(password_value) >= 8):
            ui.notify('Password must contain at least one letter, one number, and be at least 8 characters long.', color='negative')
            return
        
        #add username chekcs
        
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go

        else:
            ui.notify('somthing wrong', color='negative')


        # Existing login logic

    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=try_login)
        ui.button('signup',on_click=lambda: ui.open('signup'))
        ui.link('Forgot Password?' , '/forgot_password')  # Link to the "Forgot Password" page

>>>>>>> parent of 0abc1cc (renew gui.)

