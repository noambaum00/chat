# chat_selection_screen.py
import asyncio
from nicegui import ui
@ui.page("/chat_list")
async def chat_selection_screen():
    ui.text('Chat Selection Screen'),
    ui.dropdown('Select Room:', options=get_room_list(), on_change=room_dropdown_change),
    ui.textbox('Join New Room:'),
    ui.button('Join', on_click=join_button_click),
    ui.button('Back', on_click=back_button_click),


def get_room_list():
    # Add API call to get user rooms here
    # For now, returning sample data
    return ['Room 1', 'Room 2', 'Room 3']

async def room_dropdown_change(value):
    ui.message(f'Selected room: {value}')

async def join_button_click():
    selected_room = ui.get_value('Select Room:')
    new_room = ui.get_value('Join New Room:')
    
    if new_room:
        create_new_room = ui.confirm('Room does not exist. Do you want to create a new room?')
        if create_new_room:
            # Add API call to create new room here
            ui.message(f'Creating new room: {new_room}')
    else:
        ui.message(f'Joining existing room: {selected_room}')

async def back_button_click():
    ui.message('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
