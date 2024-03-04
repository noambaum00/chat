# login_screen.py
import asyncio
from nicegui import ui, app
from api_reqest import api
import json

global username
global password

@ui.page("/login")
async def login_screen():
    global username
    global password

    ui.label('Login Screen')
    username = ui.input('Username:').on('keydown.enter', login_button_click).props('input-style="color: blue" input-class="font-mono"')
    password = ui.input('Password:', password=True).on('keydown.enter', login_button_click).props('input-style="color: blue" input-class="font-mono"')

    ui.button('Login', on_click=login_button_click)
    ui.button('Back', on_click=back_button_click)

async def login_button_click():
    global username
    global password

    # Retrieve username and password values
    username_value = username.value
    password_value = password.value

    # Check if username or password is empty
    if not username_value or not password_value:
        ui.notify('Please enter both username and password', color="red")
        return

    # Prepare data for API request
    mydata = {
        "username": username_value,
        "password": password_value
    }
    try:
        # Make API request
        response = api("POST", "api/users/login", data=mydata)
    except:
        ui.notify("error acured, try agan later", color="red")
    # Check for errors in the response
    if isinstance(response, dict) and 'access_token' in response:
        # Successful login
        app.storage.user['access_token'] = response['access_token']
        app.storage.user['username'] = username_value  # Store username in user storage
        ui.open('/chat_list')  # Redirect to dashboard upon successful login
    else:
        # Failed login
        error_message = response.get('message') if isinstance(response, dict) else 'Unknown error'
        ui.notify(f'Login failed: {error_message}', color='red')

async def back_button_click():
    ui.notify('Redirecting to Home Screen')
    ui.open("/")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(storage_secret='your_private_key')
