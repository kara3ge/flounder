from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import time
import python.stats as stats
import python.terminal as terminal
import json
from config import config
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = config["flounder-secet-key"] #should be environ but xdd

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = True


@app.route('/')
def login():
    return render_template("login.html")

@app.route("/authcheck", methods=["POST"])
def authcheck():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        if not password.isalnum() or not username.isalnum():
            return redirect(url_for("login"))
        valid = check_password_hash(config["login-key"], password)
        if valid: 
            session["user_id"] = username
            session["valid"] = True
            session["access-time"] = str(datetime.now())
            return redirect(url_for("home"))
        else:
            print("invalid password:", password)
            return redirect(url_for("login"))
    except Exception as e:
        print(e, "data = ",request.data.decode('utf-8'), "eof")
        return redirect(url_for("login"))
    

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/terminal/command', methods=['POST'])
def terminal_command():
    try:
        command =  json.loads(request.data.decode('utf-8'))["command"]
        print("command:", command)
        output = terminal.execute_command(command)
        print("out:", output)
        if "error" in output:
            print("error:", output["error"])
            return jsonify({'error': output["error"]}), 500
        return jsonify({'stdout': output["stdout"]})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/graphs/info_update')
def info_update():
    data = {
        "cpu_usage": stats.get_cpu_usage(),
        "gpu_usage": stats.get_gpu_usage(),
        "memory_usage": stats.get_memory_usage(),
        "disk_usage": stats.get_disk_usage(),
        "network_usage": stats.get_network_usage(),
        "temperature": stats.get_temperature(),
        "last_update": str(datetime.now())
    }
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
