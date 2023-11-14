from nicegui import Client, app, ui
from pydantic import BaseModel, EmailStr
import re
class Email(BaseModel):
    email: EmailStr


from pydantic import BaseModel, EmailStr
import bcrypt
from pydantic import BaseModel, EmailStr

class SignupForm(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str

@ui.page('/signup')
def signup() -> None:
    def try_signup() -> None:
        # Validate the signup form
        try:
            signup_form = SignupForm(
                username=username.value,
                password=password.value,
                email=email.value,
                phone=phone.value
            )
        except ValueError as e:
            ui.notify(f'Invalid input: {str(e)}', color='negative')
            return

        # Additional password security checks
        if not (any(char.isdigit() for char in signup_form.password) and any(char.isalpha() for char in signup_form.password) and len(signup_form.password) >= 8):
            ui.notify('Password must contain at least one letter, one number, and be at least 8 characters long.', color='negative')
            return

        # Hash the password before storing
        hashed_password = bcrypt.hashpw(signup_form.password.encode('utf-8'), bcrypt.gensalt())

        # Implement your signup logic here, storing hashed_password instead of plain text password
        # You may want to store new user credentials in a database
        # For example: users_collection.insert_one({'username': signup_form.username, 'password': hashed_password, 'email': signup_form.email, 'phone': signup_form.phone})
        ui.notify(f'User {signup_form.username} signed up successfully!', color='positive')

    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        email = ui.input('Email', type='email')
        phone = ui.input('Phone', type='tel')
        ui.button('Sign Up', on_click=try_signup)
        ui.button('Login', on_click=lambda: ui.open('/login'))
