from flask import Flask, render_template, request, redirect, url_for, session
from uuid import UUID
import json
from functools import wraps

# Carregar o arquivo JSON
with open('env.json') as f:
    env = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = env["system"]["secretKey"]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_logged"):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function