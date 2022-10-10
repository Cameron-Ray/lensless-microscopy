#Import necessary libraries
import datetime
import os

import CloudFlare
import cv2
from dotenv import load_dotenv
from flask import Flask, Response, render_template
from requests import get

#Initialize the Flask app
app = Flask(__name__)

#Load Cloudflare API token
load_dotenv()
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
currentTime = datetime.now()
oldTime = currentTime

camera = cv2.VideoCapture(0)

def refreshDNS():
    currentTime = datetime.now()
    if currentTime > oldTime + datetime. timedelta(hours=1):
        cf = CloudFlare.CloudFlare(token=CLOUDFLARE_API_TOKEN)
        zones = cf.zones.get(params={"name": "cameronray.co.za"})
        zone_id = zones[0]["id"]
        a_record = cf.zones.dns_records.get(zone_id, params={"name": "rpi-microscope.cameronray.co.za", "type": "A"})[0] 
        a_record["ttl"] = 60
        ip = get('https://api.ipify.org').content.decode('utf8')
        a_record["content"] = ip
        cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)
        oldTime = datetime.now()


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    refreshDNS()
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    refreshDNS()
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="192.168.0.164",port="80")
