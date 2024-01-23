# home_screen.py
import asyncio
from nicegui import ui

@ui.page("/")
async def home_screen():
    with ui.grid():  # Set alignment to center
        ui.label('Welcome to the chiity'),
        ui.button('Login', on_click=login_button_click),
        ui.button('Sign In', on_click=sign_in_button_click),
        ui.button('Password Reset', on_click=password_reset_button_click),

async def login_button_click():
    ui.notify('Redirecting to Login Screen', on_click=lambda: ui.open("login", new_tab=True))
    

async def sign_in_button_click():
    ui.notify('Redirecting to Sign In Screen')

async def password_reset_button_click():
    ui.notify('Redirecting to Password Reset Screen')



if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
