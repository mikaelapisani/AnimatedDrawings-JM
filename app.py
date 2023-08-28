
from distutils.log import debug
from fileinput import filename
from flask import *  
import subprocess
import time
import shutil



app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subir_imagen', methods=['POST'])
def character():
    if request.method == 'POST':  
        f = request.files['file']
        f.save('image.png')
        # ts stores the time in seconds
        ts = str(time.time())
        shutil.copy('image.png', f'images/{ts}.png')
        p = subprocess.run(["python3.8", "image_to_animation.py", "image.png", 'static/output'])
        shutil.copy('static/output/video.gif', f'videos/{ts}.gif')
    
    return render_template('index.html')
   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)