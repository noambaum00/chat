from nicegui import ui
from routes import home_screen, login_screen, signup_screen, password_reset_screen, chat_selection_screen, chat_view_screen
def run():
    ui.run(storage_secret='your_private_key')