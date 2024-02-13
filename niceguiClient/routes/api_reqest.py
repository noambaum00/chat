import requests

URL = "http://localhost:5000/"

def api(method, path, data="", headers=""):
    switch_dict = {
        "GET": get,
        "POST": post,
        "DELETE": delete,
        "PUT": put
    }
    return switch_dict.get(method, default)(path, data, headers)

def get(path, data="", headers=""):
    response = requests.get(URL + path, params=data, headers=headers)
    return handle_response(response)

def post(path, data="", headers=""):
    response = requests.post(URL + path, json=data, headers=headers)
    return handle_response(response)

def delete(path, data="", headers=""):
    response = requests.delete(URL + path, params=data, headers=headers)
    return handle_response(response)

def put(path, data="", headers=""):
    response = requests.put(URL + path, json=data, headers=headers)
    return handle_response(response)

def default(path, data="", headers=""):
    return ""

def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
