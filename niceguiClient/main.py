import asyncio
from nicegui import ui
from login import LoginScreen
from register import RegisterScreen
from chat_selection import ChatSelectionScreen
from chat_view import ChatViewScreen

async def main():
    login_screen = LoginScreen()
    register_screen = RegisterScreen()
    chat_selection_screen = ChatSelectionScreen()
    chat_view_screen = ChatViewScreen()

    ui.stacked(layout='vbox', items=[
        login_screen,
        register_screen,
        chat_selection_screen,
        chat_view_screen
    ])

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
