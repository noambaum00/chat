from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

from pydantic import BaseModel, EmailStr

import re

class Email(BaseModel):
    email: EmailStr


# in reality users' passwords would obviously need to be hashed
passwords = {'user1': '1234567q', 'user2': 'pass2'}

unrestricted_page_routes = {'/login', '/signup', '/forgot_password'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/')
def main_page() -> None:
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=lambda: (app.storage.user.clear(), ui.open('/login')), icon='logout').props('outline round')


@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')


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
        ui.button('/login',on_click=lambda: ui.open('login'))


@ui.page('/forgot_password')
def forgot_password() -> None:
    def recover_password() -> None:
        # Validate the email input
        try:
            email_model = Email(email=email.value)
        except ValueError as e:
            ui.notify(f'Invalid email address: {str(e)}', color='negative')
            return

        # Implement your password recovery logic here
        ui.notify(f'Password recovery email sent to {email_model.email}!', color='positive')

    with ui.card().classes('absolute-center'):
        email = ui.input('Email')
        ui.button('Recover Password', on_click=recover_password)


ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
