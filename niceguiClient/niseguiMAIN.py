
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui
import clientDefine

# in reality users' passwords would obviously need to be hashed
passwords = {'user1': '1234567q', 'user2': 'pass2'}

unrestricted_page_routes = {'/login', '/signup', '/forgot_password'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)



@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')



ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')
