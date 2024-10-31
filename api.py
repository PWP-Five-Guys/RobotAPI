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
logging.basicConfig(filename='api_output.log', level=logging.DEBUG)  # Enable debug-level logging

def ssh_command_to_pi(command):
    """SSH into the Raspberry Pi and run the motor command."""
    try:
        logging.info(f"Connecting to {PI_HOST} via SSH...")
        # Initialize SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(PI_HOST, username=PI_USERNAME, password=PI_PASSWORD)
        kill_command = "pkill -f main.py"
        logging.info(f"Executing Kill Command: {kill_command}")
        client.exec_command(kill_command)
        # Command to execute the correct Python script on the Pi
        ssh_command = f'python3 "bcm2835-1.70/Motor_Driver_HAT_Code/Motor_Driver_HAT_Code/Raspberry Pi/python/main.py" {command}'
        logging.info(f"Executing SSH Command: {ssh_command}")

        # Execute the command on the Pi
        stdin, stdout, stderr = client.exec_command(ssh_command)

        # Capture and log output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if output:
            logging.info(f"SSH Output: {output}")
            print(f"SSH Output: {output}")
        if error:
            logging.error(f"SSH Error: {error}")
            print(f"SSH Error: {error}")

    except Exception as e:
        logging.error(f"SSH Connection failed: {e}")
        print(f"SSH Connection failed: {e}")
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
    content = request.json
    command = content['in_command'][0]  # Extract the command ("forward", "stop", etc.)

    logging.info(f"Received command: {command}")
    ssh_command_to_pi(command)  # Send the command to the Pi over SSH

    response = {'success': True, 'out_command': command}
    return jsonify(response)

# Route to fetch and stream the log files
@app.route('/logs/<filename>')
def logs(filename):
    """Serve the log files dynamically."""
    log_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(log_path):
        return send_file(log_path, mimetype='text/plain')
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=10000)
