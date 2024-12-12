import os
import logging
from flask import Flask, render_template, Response, jsonify, request

# Flask setup
app = Flask(__name__)

# Logging setup
logging.basicConfig(filename='api_output.log', level=logging.DEBUG)
log = logging.getLogger("werkzeug")
log.disabled = True  

import cv2
camera = cv2.VideoCapture(0)

# Routes
@app.route('/')
def home():
    """Serve the main interface."""
    return render_template('index.html')


def generate_frames():
    """Generator for camera frames."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Stream the video feed to the interface."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logs/<filename>', methods=['GET'])
def logs(filename):
    """Serve log files dynamically."""
    log_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            return file.read(), 200, {'Content-Type': 'text/plain'}
    else:
        return jsonify({'error': 'Log file not found'}), 404


@app.route('/move', methods=['POST'])
def move():
    """Handle robot movement commands."""
    content = request.json
    command = content.get('command')
    if command:
        logging.info(f"Received command: {command}")
        return jsonify({'success': True, 'command': command}), 200
    else:
        return jsonify({'error': 'Invalid command'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
