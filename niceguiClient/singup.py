from nicegui import Client, app, ui
from pydantic import BaseModel, EmailStr
import re
class Email(BaseModel):
    email: EmailStr


@ui.page('/signup')
def signup() -> None:
    def try_signup() -> None:
        # Implement your sign-up logic here
        # You may want to store new user credentials in the 'passwords' dictionary
        ui.notify(f'User {username.value} signed up successfully!', color='positive')

    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Sign Up', on_click=try_signup)
        ui.button('login',on_click=lambda: ui.open('login'))
