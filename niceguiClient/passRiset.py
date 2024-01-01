from nicegui import Client, app, ui
from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    email: EmailStr

@ui.page('/forgot_password')
def forgot_password() -> None:
    def recover_password() -> None:
        # Validate the email input
        try:
            email_model = Email(email=email.value)
        except ValueError as e:
            ui.notify(f'Invalid email address: {str(e)}', color='negative')
            return

        # Implement your password recovery logic here
        ui.notify(f'Password recovery email sent to {email_model.email}!', color='positive')

    with ui.card().classes('absolute-center'):
        email = ui.input('Email')
        ui.button('Recover Password', on_click=recover_password)