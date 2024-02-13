# chat_selection_screen.py
import requests

import asyncio
from nicegui import ui
@ui.page("/chat_list")
async def chat_selection_screen():
    ui.label('Chat Selection Screen'),
    ui.select(get_room_list(), on_change=room_dropdown_change)
    ui.label('Join New Room:'),
    ui.input("Room name: ")
    ui.button('Join', on_click=join_button_click),
    ui.button('Back', on_click=back_button_click),


def get_room_list():
    # Add API call to get user rooms here
    # For now, returning sample data
    url = "http://localhost:5000/api/rooms"
    return list(requests.get(url).json())




async def room_dropdown_change(value):
    ui.notify(f'Selected room: {value}')

async def join_button_click():
    #selected_room = ui.get_value('Select Room:')
    #new_room = ui.get_value('Join New Room:')


    if (room_name in list(requests.get(url).json())):
        create_new_room = ui.confirm('Room does not exist. Do you want to create a new room?')
        if create_new_room:
            response = requests.post(url, json = data_to_send)
            ui.notify(str(response.json()))
            ui.notify(f'Creating new room: {new_room}')
    else:
        ui.notify(f'Joining existing room: {selected_room}')

async def back_button_click():
    ui.notify('Redirecting to Home Screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()