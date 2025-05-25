from routes import app
from main import env

app.run(
    debug=env["system"]["debug"],
    host=env["system"]["host"],
    port=env["system"]["port"]
)