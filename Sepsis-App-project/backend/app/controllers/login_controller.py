from flask import request, jsonify

# Fake user để test
USERS = {
    "admin": "123456",
    "user": "password"
}

def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in USERS and USERS[username] == password:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {"username": username}
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401
