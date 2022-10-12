#Import necessary libraries
import datetime
import os
import platform
import socket
import threading
from time import sleep

import CloudFlare
import cv2
from dotenv import load_dotenv
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from requests import get

# Load Cloudflare API token
load_dotenv()
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')

# Initialize the Flask app
app = Flask(__name__)

if platform.system().lower() == 'linux':
    camera = cv2.VideoCapture('/dev/video0')
else:
    camera = cv2.VideoCapture(0)

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

# def refresh_DNS_thread():
#     # Update DNS record IP address on 30min interval
#     while(1):
#         # Create Cloudflare object with API token
#         cf = CloudFlare.CloudFlare(token=CLOUDFLARE_API_TOKEN)

#         # Get zones and cameronray.co.za zone ID
#         zones = cf.zones.get(params={"name": "cameronray.co.za"})
#         zone_id = zones[0]["id"]

#         # Get the existing A record for rpi-microscope subdomain
#         a_record = cf.zones.dns_records.get(zone_id, params={"name": "rpi-microscope.cameronray.co.za", "type": "A"})[0] 
#         a_record["ttl"] = 60
#         ip = get('https://api.ipify.org').content.decode('utf8')

#         # Only update A record if the IP has changed
#         if (a_record["content"] != ip):
#             a_record["content"] = ip
#             cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)
#             app.logger.info('DNS record updated successfully!')

#         sleep(10)


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
    return render_template('index.html')

@app.route('/historical-images')
def historical_images():
    return render_template('historical_images.html')

@app.route('/image-capture')
def image_capture():
    return render_template('image_capture.html', methods=('GET', 'POST'))

@app.route('/load-sample')
def sample_load():
    return render_template('sample_load.html')


@app.route('/video_feed')
def video_feed():
    # Return the video buffer
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Host the flask app on the Pi's local IP address
# The port 80 is forwarded on a local router to expose the
# web server to the internet
if __name__ == "__main__":
    # Optional Dynamic DNS update
    # DNS_update_thread = threading.Thread(target=refresh_DNS_thread, daemon=True)
    # DNS_update_thread.start()
    app.run(debug=True, host=get_local_IP(), port="80")
