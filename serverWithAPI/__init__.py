# app/__init__.py
from .defines import Defines
from flask import Flask, jsonify, url_for
from flask_restful import Resource
from .routes import room_management, user_management
#from .api_info import ApiInfo
from .blueprint import *

from defines import Defines
#import defines

defines.const = Defines()

# Register blueprints
app.register_blueprint(user_management, url_prefix='/api')
app.register_blueprint(room_management, url_prefix='/api')

#Api.add_resource(ApiInfo, '/api/info', endpoint='api_info')

if __name__ == '__main__':
    app.run(debug=True)
    print(app.url_map.iter_rules())
