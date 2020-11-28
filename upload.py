from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import webbrowser
from threading import Timer
import OCR_text

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
# Provide the image destination path 
app.config['UPLOADED_PHOTOS_DEST'] = 'C:/Users/SA20111930/Assessment/OCR_based_web_app_flask_SAYAN_HAZRA/Image'
configure_uploads(app, photos)

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/upload')

# The images are stored in /Images/ folder
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        text = OCR_text.extract_text(filename)
        output = f'NAME: {text[0]}<br/><br/>DateOfBirth: {text[1]}<br/><br/>PANNumber: {text[2]}'
        return '<h1>Detected PAN Card Credentials</h1><br/>'+output
    return render_template('upload.html')

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run(port = 5000, debug = True)
