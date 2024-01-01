from nicegui import Client, app, ui

@ui.page('/')
def main_page() -> None:
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=lambda: (app.storage.user.clear(), ui.open('/login')), icon='logout').props('outline round')
