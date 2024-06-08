import cv2
import os
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def remove_background(input_path,output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/remback',methods=['POST'])
def remback():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        rembg_img_name = filename.split('.')[0]+"_rembg.png"
        remove_background(UPLOAD_FOLDER+'/'+filename,UPLOAD_FOLDER+'/'+rembg_img_name)
        return render_template('home.html',org_img_name=filename,rembg_img_name=rembg_img_name)


if __name__ == '__main__':
    app.run(debug=True)