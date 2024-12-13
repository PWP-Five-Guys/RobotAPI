from flask import Flask, Response

import cv2


app = Flask(__name__)


# Initialize the camera

camera = cv2.VideoCapture(0)  # Use 0 for the default camera


@app.route('/video_feed')

def video_feed():

    def generate():

        while True:

            success, frame = camera.read()  # Read a frame from the camera

            if not success:

                break

            _, buffer = cv2.imencode('.jpg', frame)  # Encode the frame to JPEG

            yield (b'--frame\r\n'

                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')  # Send the frame in HTTP response

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')

def index():

    return '''

        <html>

            <head>

                <title>Video Stream</title>

            </head>

            <body>

                <h1>Live Video Feed</h1>

                <img src="/video_feed" width="640" height="480">

            </body>

        </html>

    '''


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=59000)
