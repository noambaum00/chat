# Define user roles and associated privileges
global ROLES
ROLES = {
    'user': ['read_messages', 'send_messages', 'add_rooms','see_room', 'change_password'],
    'admin': ['read_messages', 'send_messages', 'manage_users', 'manage_rooms', 'start_service', 'close_service', 'force_change_password'],
}
def init():
    global app
    global db
    global jwt
    app=None
    jwt=None
    db=None
