#Import necessary libraries
import datetime
import os
import platform
import socket
import subprocess
import threading
from time import sleep
from gpiozero import CPUTemperature
import RPi.GPIO as GPIO

import cv2
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from sample import Sample
from requests import get

# Initialize the Flask app
app = Flask(__name__)

bacterial_sample = Sample(None, None, None, colony_count=None)

camera = cv2.VideoCapture('/dev/video0')
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 480
height = 480
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

bg_path = '/home/pi/microscope/backgrounds'
im_path = '/home/pi/microscope/images'

LED_Pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_Pin, GPIO.OUT)
GPIO.output(LED_Pin, 1)

def get_local_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def gen_frames():  
    while True:
        # Read a camera frame 
        success, frame = camera.read()
        if not success:
            break
        else:
            # Use CV2 to encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Add frame to output
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

@app.route('/')
def index():
    ssid = os.popen('iwgetid').read().split('"')[1]

    uptime = os.popen('uptime -p').read()[3:-1]
    uptime = uptime.lower()
    uptime = uptime.replace(" minutes", "m")
    uptime = uptime.replace(" hours", "h")
    uptime = uptime.replace(" days", "d")
    uptime = uptime.replace(",", "")

    rpi_diagnostics = {"temp": CPUTemperature().temperature, "ssid": ssid, "uptime": uptime}

    return render_template('index.html', bacterial_sample = bacterial_sample, rpi_diagnostics = rpi_diagnostics)

@app.route('/historical-images')
def historical_images():
    return render_template('historical_images.html')

@app.route('/image-capture')
def image_capture():
    return render_template('image_capture.html', methods=('GET', 'POST'))

@app.route('/load-sample', methods = ['POST', 'GET'])
def load_sample():
    global camera
    global bg_path
    global im_path
    global bacterial_sample

    if request.method == 'GET':
        data = {"bg_cap": False, "sample_id": "", "colony_count": "", "growth": ""}
        return render_template('sample_info.html', data = data)

    elif request.method == 'POST':
        data = {"bg_cap": False, "sample_id": request.form["sample-id"], "colony_count": request.form["count"], "growth": request.form["growth-data"]}
        
        if request.form["sample-id"] == "":
            return render_template('sample_info.html', data = data)            
        else:
            # Capture image
            check, frame = camera.read()

            # Convert to Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Crop Image to a square
            height = len(frame[:,0])
            width = len(frame[0,:])
            crop_start_x = (width - height)//2
            frame = frame[:,crop_start_x:crop_start_x + height]

            # Save Image
            filename = request.form["sample-id"] + ".jpg"
            bg_img_path = os.path.join(bg_path, filename)
            cv2.imwrite(bg_img_path, frame)

            data["bg_cap"] = True
            bacterial_sample = None

            #TODO: Add functionality to load predefined data
            bacterial_sample = Sample(data["sample_id"], {}, datetime.datetime.now())

            return render_template('sample_info.html', data = data)

@app.route('/background-capture')
def background_capture():
    print("Background captured!")
    return ("nothing")

@app.route('/video-feed')
def video_feed():
    # Return the video buffer
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Host the flask app on the Pi's local IP address
# The port 80 is forwarded on a local router to expose the
# web server to the internet
if __name__ == "__main__":
    app.run(debug=False, host=get_local_IP(), port="80")
