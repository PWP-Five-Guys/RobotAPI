import pickle
from flask import Flask, jsonify, request, render_template, send_file, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import logging
import os
import asyncio
import websockets
import base64
import cv2

# SSH details
PI_HOST = "192.168.240.19"
PI_USERNAME = "pi"
PI_PASSWORD = "5guys"

# Flask setup
app = Flask(__name__)
user_logged_in = False
app.secret_key = 'gJwlRqBv959595'
logging.basicConfig(filename='api_output.log', level=logging.DEBUG)

# Store the last command in memory for easy access
last_command = None

users_file = 'users.pkl'
if not os.path.exists(users_file):
    # Create the file if it doesn't exist
    open(users_file, 'wb').close()

def save_to_pkl(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_from_pkl(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except EOFError:
        return []

def ssh_command_to_pi(command):
    """SSH into the Raspberry Pi and run the motor command."""
    try:
        kill_command = f'pkill -f "../bcm2835-1.70/Motor_Driver_HAT_Code/Motor_Driver_HAT_Code/Raspberry Pi/python/main.py"'
        os.system(kill_command)
        stop_command = f'python3 "../bcm2835-1.70/Motor_Driver_HAT_Code/Motor_Driver_HAT_Code/Raspberry Pi/python/main.py stop"'
        os.system(stop_command)
        ssh_command = f'python3 "../bcm2835-1.70/Motor_Driver_HAT_Code/Motor_Driver_HAT_Code/Raspberry Pi/python/main.py" {command}'
        logging.info(f"Executing SSH Command: {ssh_command}")
        os.system(ssh_command)
    except Exception as e:
        logging.error(f"SSH Connection failed: {e}")

@app.route('/', methods=['GET', 'POST'])
def login_register():
    global user_logged_in
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            form_type = data.get('form_type')
            
            if form_type == 'login':
                username_or_email = data.get('username_or_email')
                password = data.get('password')
                users = load_from_pkl(users_file)
                user = next((u for u in users if u['username'] == username_or_email or u['email'] == username_or_email), None)

                if user and check_password_hash(user['password'], password):
                    user_logged_in = True
                    return jsonify(success=True, redirect_url=url_for('home'))
                else:
                    return jsonify(success=False, message="Invalid username/email or password")
            
            elif form_type == 'register':
                name = data.get('name')
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                users = load_from_pkl(users_file)

                if any(u['username'] == username for u in users):
                    return jsonify(success=False, message="Username already exists")
                elif any(u['email'] == email for u in users):
                    return jsonify(success=False, message="Email already exists")
                else:
                    hashed_password = generate_password_hash(password)
                    users.append({'name': name, 'username': username, 'email': email, 'password': hashed_password})
                    save_to_pkl(users, users_file)
                    return jsonify(success=True, message="Registration successful! Please log in.")

    return render_template('login.html')

@app.route('/home')
def home():
    if user_logged_in:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/move', methods=['POST'])
def move():
    """Handle POST requests to move the robot."""
    global last_command
    content = request.json
    command = content.get('in_command', [None])[0]

    if command:
        logging.info(f"Received command: {command}")
        ssh_command_to_pi(command)
        last_command = command
        return jsonify({'success': True, 'out_command': command}), 200
    else:
        return jsonify({'error': 'Invalid command'}), 400

@app.route('/move', methods=['GET'])
def get_last_command():
    """Handle GET requests to retrieve the last command sent to the robot."""
    if last_command:
        return jsonify({'last_command': last_command}), 200
    else:
        return jsonify({'message': 'No command sent yet'}), 200

@app.route('/logs/<filename>', methods=['GET'])
def logs(filename):
    """Serve the log files dynamically."""
    log_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(log_path):
        return send_file(log_path, mimetype='text/plain')
    else:
        return jsonify({'error': 'File not found'}), 404

# WebSocket-based video feed
async def handle_connection(websocket, path):
    """
    WebSocket connection handler.
    """
    for frame in get_frames():
        await websocket.send(frame)

def get_frames():
    """
    Generator function to yield byte-encoded frames for streaming.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.png', frame)
            frame = base64.b64encode(buffer)
            yield b'data:image/png;base64,' + frame

# Start video capture
camera = cv2.VideoCapture(0)

# Start WebSocket server for video streaming
start_server = websockets.serve(handle_connection, "0.0.0.0", 8000)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_server)
    app.run(host="0.0.0.0", debug=True, port=10000)
