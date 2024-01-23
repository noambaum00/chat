# chat_view_screen.py
import asyncio
from nicegui import ui

async def chat_view_screen():
    ui.text('Chat View Screen'),
    ui.chat(messages=get_chat_history()),
    ui.textbox('Type your message:', on_change=message_input_change),
    ui.button('Send', on_click=send_button_click),
    ui.button('Back', on_click=back_button_click),


def get_chat_history():
    # Add API call to get chat history here
    # For now, returning sample data
    return [
        dict(text='Hello NiceGUI!', name='Robot', stamp='now', avatar='https://robohash.org/ui'),
        dict(text='Hi there!', name='User', stamp='now', avatar='https://robohash.org/user'),
    ]

async def message_input_change(value):
    ui.message(f'Typed message: {value}')

async def send_button_click():
    typed_message = ui.get_value('Type your message:')
    # Add API call to send message here
    ui.chat_message(typed_message, name='User', stamp='now', sent=True)

async def back_button_click():
    ui.message('Redirecting to Chat Selection Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
