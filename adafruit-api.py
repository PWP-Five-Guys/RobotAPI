from flask import Flask, jsonify, request
from adafruit_motorkit import MotorKit
import time

# Initialize Flask and MotorKit
app = Flask(__name__)
kit = MotorKit(0x40)  # I2C address for Motor HAT

# Movement control functions
def forward(duration):
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = 0.64
    time.sleep(duration)
    stop()

def backward(duration):
    kit.motor1.throttle = 0.7
    kit.motor2.throttle = -0.7
    time.sleep(duration)
    stop()

def left(duration):
    kit.motor1.throttle = -0.64
    kit.motor2.throttle = -0.64
    time.sleep(duration)
    stop()

def right(duration):
    kit.motor1.throttle = 0.64
    kit.motor2.throttle = 0.64
    time.sleep(duration)
    stop()

def stop():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

# Flask route to handle movement commands
@app.route('/move', methods=['POST'])
def move():
    content = request.json
    command = content['in_command'][0]  # Command type
    duration = float(content['in_command'][1])  # Duration in seconds

    # Execute the appropriate command
    if command == "forward":
        forward(duration)
    elif command == "backward":
        backward(duration)
    elif command == "left":
        left(duration)
    elif command == "right":
        right(duration)
    else:
        stop()

    response = {'success': True, 'out_command': command}
    return jsonify(response)

# Run the Flask app on 0.0.0.0 to accept connections from the network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
