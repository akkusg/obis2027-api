import hmac
import os

from flask import Flask, jsonify, request, session


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    API_USERNAME=os.environ.get("API_USERNAME"),
    API_PASSWORD=os.environ.get("API_PASSWORD"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE") == "true",
)

COURSES = [
    {"code": "MAT101", "name": "Matematik"},
    {"code": "BIL101", "name": "Bilgisayara Giriş"},
]


@app.post("/api/login")
def login():
    if not all(app.config.get(key) for key in ("SECRET_KEY", "API_USERNAME", "API_PASSWORD")):
        return jsonify(error="API kimlik doğrulaması yapılandırılmamış"), 503

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not all(
        isinstance(data.get(key), str) and data[key] for key in ("username", "password")
    ):
        return jsonify(error="Kullanıcı adı ve parola gereklidir"), 400

    username_matches = hmac.compare_digest(
        data["username"].encode(), app.config["API_USERNAME"].encode()
    )
    password_matches = hmac.compare_digest(
        data["password"].encode(), app.config["API_PASSWORD"].encode()
    )
    if not (username_matches and password_matches):
        return jsonify(error="Kullanıcı adı veya parola hatalı"), 401

    session.clear()
    session["authenticated"] = True
    return jsonify(message="Giriş başarılı")


@app.get("/api/list-courses")
def list_courses():
    if not session.get("authenticated"):
        return jsonify(error="Giriş yapmanız gerekiyor"), 401
    return jsonify(courses=COURSES)
