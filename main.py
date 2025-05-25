from flask import Flask, render_template, request, redirect, url_for
from uuid import UUID
import json

# Carregar o arquivo JSON
with open('env.json') as f:
    env = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'