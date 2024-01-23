# password_reset_screen.py
import asyncio
from nicegui import ui

def password_reset_screen():
    ui.text('Password Reset Screen'),
    ui.input('Email:'),
    ui.button('Reset Password', on_click=reset_password_button_click),
    ui.button('Back', on_click=back_button_click),

async def reset_password_button_click():
    email = ui.get_value('Email:')
    # Add API call for password reset here
    ui.message(f'Resetting password for {email}...')

async def back_button_click():
    ui.message('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
