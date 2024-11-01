from flask import Flask, jsonify, request, render_template, send_file
import paramiko
import logging
import os

# SSH details
PI_HOST = "192.168.1.121"
PI_USERNAME = "pi"
PI_PASSWORD = "5guys"

# Flask setup
app = Flask(__name__)
logging.basicConfig(filename='api_output.log', level=logging.DEBUG)

# Store the last command in memory for easy access
last_command = None

def ssh_command_to_pi(command):
    """SSH into the Raspberry Pi and run the motor command."""
    try:
        logging.info(f"Connecting to {PI_HOST} via SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(PI_HOST, username=PI_USERNAME, password=PI_PASSWORD)
        
        # Kill any previous instances of the script
        kill_command = "pkill -f main.py"
        logging.info(f"Executing Kill Command: {kill_command}")
        client.exec_command(kill_command)
        
        # Execute the command on the Pi
        ssh_command = f'python3 "bcm2835-1.70/Motor_Driver_HAT_Code/Motor_Driver_HAT_Code/Raspberry Pi/python/main.py" {command}'
        logging.info(f"Executing SSH Command: {ssh_command}")
        stdin, stdout, stderr = client.exec_command(ssh_command)

        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if output:
            logging.info(f"SSH Output: {output}")
        if error:
            logging.error(f"SSH Error: {error}")

    except Exception as e:
        logging.error(f"SSH Connection failed: {e}")
    finally:
        client.close()
        logging.info("SSH Connection closed.")

@app.route('/')
def home():
    """Render the control interface."""
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    """Handle POST requests to move the robot."""
    global last_command
    content = request.json
    command = content.get('in_command', [None])[0]

    if command:
        logging.info(f"Received command: {command}")
        ssh_command_to_pi(command)  # Send the command to the Pi over SSH
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

if __name__ == '__main__':
    app.run(debug=True, port=10000)
