# import the necessary packages
import os

from flask import (Flask, Response, render_template, request,
                   send_from_directory)
from imutils.video.pivideostream import PiVideoStream

from camera import VideoCamera

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
# @app.route('/picture')
# def take_picture():
#     pi_camera.take_picture()
#     return "None"

if __name__ == '__main__':

    app.run(host='192.168.0.74', debug=False)
