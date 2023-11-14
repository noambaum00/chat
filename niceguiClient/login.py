from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import Client, app, ui
from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    email: EmailStr



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
        ui.link('/forgot_password', 'Forgot Password?')  # Link to the "Forgot Password" page


