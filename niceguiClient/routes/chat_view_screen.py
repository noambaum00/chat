# chat_view_screen.py
import asyncio
from nicegui import ui

@ui.page("/chat_view/<url_room_name>")
async def chat_view_screen():
    ui.label('Chat View Screen'),
    if allow_in_room():
        ui.chat_message(messages=get_chat_history()),
        ui.textbox('Type your message:', on_change=message_input_change)
        ui.button('Send', on_click=send_button_click)
        ui.button('Back', on_click=back_button_click)


def get_chat_history():
    # Add API call to get chat history here
    # For now, returning sample data
    return [
        dict(text='Hello NiceGUI!', name='Robot', stamp='now'),
        dict(text='Hi there!', name='User', stamp='now'),
    ]

async def message_input_change(value):
    ui.notify(f'Typed message: {value}')

async def send_button_click():
    typed_message = ui.get_value('Type your message:')
    # Add API call to send message here
    ui.chat_message(typed_message, name='User', stamp='now', sent=True)

async def back_button_click():
    ui.notify('Redirecting to Chat Selection Screen')
    ui.open("chat_list")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
