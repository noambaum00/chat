# login_screen.py
import asyncio
from nicegui import ui
import requests
import json
global username
global password

@ui.page("/login")
async def login_screen():
    ui.label('Login Screen')
    username = ui.input('Username:').on('keydown.enter', login_button_click).props('input-style="color: blue" input-class="font-mono"')
    password = ui.input('Password:', password = True).on('keydown.enter', login_button_click).props('input-style="color: blue" input-class="font-mono"')

    ui.button('Login', on_click=login_button_click)
    ui.button('Back', on_click=back_button_click)


async def login_button_click():
    # Add API call for authentication here
    requests = json.dump({"" : ""})
    response = requests.get('localhost:5000/api/users/login')
    print(response)
    ui.x(f'Logging in as {username}...')

async def back_button_click():
    ui.notify('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
    
