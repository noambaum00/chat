# app/api_info.py

from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required


class ApiInfo(Resource):
    @jwt_required(optional=True)
    def get(self):
        routes = []

        for route in serverWithAPI.url_map.iter_rules():
            # Exclude static files and API info endpoint itself
            if route.endpoint not in ['static', 'api_info']:
                methods = sorted(route.methods - {'OPTIONS', 'HEAD'})
                route_info = {
                    'url': str(route),
                    'methods': methods,
                    'login_required': 'Authorization' in route.arguments,
                    'role_required': 'role' in route.arguments,
                }
                routes.append(route_info)

        return jsonify({'routes': routes})
