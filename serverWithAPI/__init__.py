# app/__init__.py

from flask import Flask, jsonify, url_for
from routes import  user_management, room_management

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_demo_purposes'

# Define user roles and associated privileges
ROLES = {
    'user': ['read_messages', 'send_messages', 'add_rooms','see_room', 'change_password'],
    'admin': ['read_messages', 'send_messages', 'manage_users', 'manage_rooms', 'start_service', 'close_service', 'force_change_password'],
}

# Register blueprints
app.register_blueprint(user_management, url_prefix='/api')
app.register_blueprint(room_management, url_prefix='/api')

@app.route('/')
def index():
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':  # Exclude static files
            routes.append({
                'url': str(rule),
                'methods': sorted(rule.methods - {'OPTIONS', 'HEAD'})
            })

    return jsonify({'routes': routes})

if __name__ == '__main__':
    app.run(debug=True)
