from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/terminal', methods=['POST'])
def terminal():
    data = request.json
    return jsonify({'status': 'ok'})

@app.route('/api/info_update')
def info_stream():
    while True:
        data = {
            "cpu_usage": 10,
            "gpu_usage": 10,
            "memory_usage": 10,
            "disk_usage": 10,
            "network_usage": 10,
            "temperature": 10,
            "last_update": time.time()
        }
        yield jsonify(data)
        time.sleep(1)
        
    return Response(info_stream(), mimetype='application/json')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
