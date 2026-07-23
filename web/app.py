from flask import Flask, render_template, jsonify
from collections import deque

app = Flask(__name__)
alerts = deque(maxlen=200)

def add_alert(alert_info: dict):
    alerts.append(alert_info)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def get_alerts():
    return jsonify(list(alerts))