# signin_screen.py
import asyncio
from nicegui import ui, app
from api_reqest import api


global username
global password
global confirm_password
global email

@ui.page("/singup")
async def signup_screen():
    global username
    global password
    global confirm_password
    global email


    ui.label('Sign In Screen')
    username = ui.input('Username:')
    password = ui.input('Password:', password=True)
    confirm_password = ui.input('Confirm Password:', password=True)
    email = ui.input('email:')
    signup_button = ui.button('Sign In', on_click=signin_button_click)
    back_button = ui.button('Back', on_click=back_button_click)

async def signin_button_click():
    username_value = username.value.strip()  # Remove leading and trailing whitespaces
    password_value = password.value.strip()
    confirm_password_value = confirm_password.value.strip()
    email_value = email.value.strip()
    
    # Check if any field is empty
    if not username_value or not password_value or not confirm_password_value:
        ui.notify('Please fill in all fields.', color='red')
        return

    # Check if passwords match
    if password_value != confirm_password_value:
        ui.notify('Passwords do not match.', color='red')
        return

    # Prepare data for API request
    mydata = {
        "username": username_value,
        "password": password_value,
        "email": email_value
    }

    # Make API request
    response = api("POST", "api/users/signup", data=mydata)

    # Check status code of the response
    status_code = response.get('status_code')
    ui.notify(status_code)
    if status_code == 200:  # OK
        # Successful registration
        app.storage.user['access_token'] = response.get('access_token')
        app.storage.user['username'] = username
        ui.notify(f'Registering user {username}...', color='green')
        ui.open('/chat_list')    # Redirect to chat_list upon successful registration
    elif status_code == 400:
        # Missing email or password
        ui.notify('Please provide both username and password.', color='red')
    elif status_code == 420:
        # User already exists
        ui.notify('User already exists.', color='red')
    else:
        # Other errors
        error_message = response.get('message') if isinstance(response, dict) else 'Unknown error'
        ui.notify(f'Registration failed: {error_message}', color='red')
async def back_button_click():
    ui.notify('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(storage_secret='your_private_key')
