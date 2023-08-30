
from distutils.log import debug
from fileinput import filename
from flask import *  
import subprocess
import time
import shutil
import cv2
import os


app = Flask(__name__)
video = cv2.VideoCapture(2)  
gif = False

@app.route('/')
def index():
    global gif
    return render_template('index.html', gif=gif)

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    global gif
    return Response(gen(video), mimetype='multipart/x-mixed-replace; boundary=frame')
   
@app.route('/next',methods=['POST'])
def next():
    global saving_video
    global gif
    gif = False
    return render_template('index.html', gif=gif)

@app.route('/capture',methods=['POST'])
def capture():
    global video
    global gif
    gif = True
    success, image = video.read()
    cv2.imwrite("image.png", image)
    ts = str(time.time())
    shutil.copy('image.png', f'images/{ts}.png')
    p = subprocess.run(["python3.8", "image_to_animation.py", "image.png", 'static/output'])
    shutil.copy('static/output/video.gif', f'videos/{ts}.gif')
    return render_template('index.html', gif=gif)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)