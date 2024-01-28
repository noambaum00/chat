# home_screen.py
import asyncio
from nicegui import ui

import login_screen, signup_screen, password_reset_screen, chat_selection_screen, chat_view_screen

@ui.page("/")
async def home_screen():
    with ui.row():
        #switch = ui.switch(lambda: )
        dark = ui.dark_mode()
        ui.colors(primary='pink')
        ui.label('Welcome to the chiity'),
        ui.link('Login', "/login"),
        ui.link('Sign In', "/singup"),
        ui.link('Password Reset', "/password_reset"),

async def login_button_click():
    ui.notify('Redirecting to Login Screen', on_click=lambda: ui.open("login", new_tab=True))
    

async def sign_in_button_click():
    ui.notify('Redirecting to Sign In Screen')

async def password_reset_button_click():
    ui.notify('Redirecting to Password Reset Screen')



if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
