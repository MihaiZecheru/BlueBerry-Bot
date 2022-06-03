from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home() -> str:
    return "Uptime Webserver for BlueBerry Bot"

def run() -> None:
  app.run(host='0.0.0.0', port=8080)

def start() -> None:
    t = Thread(daemon=True, target=run)
    t.start()