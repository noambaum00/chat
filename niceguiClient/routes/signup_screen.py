# signin_screen.py
import asyncio
from nicegui import ui

@ui.page("/singup")
async def signup_screen():
    ui.label('Sign In Screen'),
    ui.input('Username:'),
    password = ui.input('Password:', password = True)
    password = ui.input('Confirm Password:', password = True)
    ui.button('Sign In', on_click=signin_button_click),
    ui.button('Back', on_click=back_button_click),


async def signin_button_click():
    username = ui.get_value('Username:')
    password = ui.get_value('Password:')
    confirm_password = ui.get_value('Confirm Password:')
    
    # Add API call for user registration here
    if password == confirm_password:
        ui.notify(f'Registering user {username}...')
    else:
        ui.notify('Passwords do not match.')

async def back_button_click():
    ui.notify('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
