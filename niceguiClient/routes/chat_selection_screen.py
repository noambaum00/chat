# chat_selection_screen.py
from api_reqest import api

import asyncio
from nicegui import ui, app

global join_room_name
global new_room_name


@ui.page("/chat_list")
async def chat_selection_screen():
    global join_room_name
    global new_room_name

    ui.label('Chat Selection Screen'),
    ui.select(get_room_list(), on_change=room_dropdown_change)
    with ui.expansion('Join New Room:').classes('w-full'):
        join_room_name = ui.input("Room name: ")
        ui.button('Join', on_click=join_button_click)

    with ui.expansion('Add New Room:').classes('w-full'):
        new_room_name = ui.input("Room name: ")
        ui.button('Add', on_click=new_button_click)
    ui.button('Back', on_click=back_button_click)


def get_room_list():
    try:
        arr = api("GET", f"api/users/{app.storage.user['username']}/rooms")
        if type(arr) is list:
            return arr
    except:
        ui.notify("error hapend, contact the dev", color= 'red')




async def room_dropdown_change(value):
    ui.notify(f'Selected room: {value}')

async def join_button_click():
    global join_room_name
    if api("GET", f"api/roomExise/{join_room_name}"):
        create_new_room = ui.confirm('realy want to join?')
        if create_new_room:
            response = api("GET", f'/api/users/{app.storage.user['username']}/join_room')
            ui.notify(str(response.json()))
            ui.notify(f'Creating new room: {new_room}')
    else:
        ui.notify('there is no rooom in this name try to add one')


async def new_button_click():
    global new_room_name
    if not api("GET", f"api/roomExise/{new_room_name}"):
        create_new_room = ui.confirm('Room does not exist. Do you want to create a new room?')
        if create_new_room:
            response = requests.post(url, json = data_to_send)
            ui.notify(str(response.json()))
            ui.notify(f'Creating new room: {new_room}')
    else:
        ui.notify(f'Joining existing room: {selected_room}')

async def back_button_click():
    ui.notify('Redirecting to Home Screen')
    ui.open("/")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()