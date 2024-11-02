# Robot Control API and Frontend

This project is a simple web interface to control a robot using commands like **forward**, **backward**, **left**, **right**, and **stop**. The commands are sent to a Flask backend via a POST request, and the backend returns a binary-encoded response representing the movement. 

## How It Works

1. **Frontend**: 
    - The frontend consists of buttons for robot movement, and a form that collects power and time inputs from the user.
    - The form submits the command to the Flask backend via a POST request in JSON format.
    
2. **Backend**:
    - The Flask backend processes the command and returns a binary-encoded string representing the direction, power, and time.
    - The **stop** command returns a binary string of all zeros, while other commands return binary strings based on power and time values.
    
3. **Binary Encoding**:
    - The first 2 bits represent the direction:
        - `00` = Forward
        - `01` = Backward
        - `10` = Left
        - `11` = Right
    - The next 8 bits represent the power value (0-255).
    - The final 8 bits represent the time value in seconds (0-255).
    - For the **stop** command, the binary string returned is always `0000000000000000`.

## Setup Instructions

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)

### Steps

1. Clone the repository or download the files.
   
2. Install Flask by running:
   ```bash
   pip install flask
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```
   
4. Open a web browser and go to `http://127.0.0.1:5000/`.