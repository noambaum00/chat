import asyncio
import websockets
from aiohttp import web
from nicegui import ui
from login import LoginScreen
from register import RegisterScreen
from chat_selection import ChatSelectionScreen
from chat_view import ChatViewScreen

async def main(request):
    login_screen = LoginScreen(api_url='http://localhost:5000')
    register_screen = RegisterScreen(api_url='http://localhost:5000')
    chat_selection_screen = ChatSelectionScreen(api_url='http://localhost:5000')
    chat_view_screen = ChatViewScreen(api_url='http://localhost:5000')

    ui.stacked(layout='vbox', items=[
        login_screen,
        register_screen,
        chat_selection_screen,
        chat_view_screen
    ])

    return web.Response(text="NiceGUI Server is Running")

if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', main)

    loop = asyncio.get_event_loop()

    # HTTP server
    web.run_app(app, host="127.0.0.1", port=8080)

    # WebSocket server
    start_server = websockets.serve(handler, "localhost", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()
