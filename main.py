from flask import Flask, render_template, request
from colorfinder import most_common_colors, rgb_to_hex
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['SECRET_KEY'] = 'pudge22211'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set the upload folder directly


def save_uploaded_file(file):
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = save_uploaded_file(file)
        if filename:
            img = Image.open(file)
            colors = most_common_colors(img)
            hex_colors = [rgb_to_hex(rgb) for rgb in colors]
            return render_template('result.html', colors=hex_colors, filename=filename)
    return "Error occurred while processing the file."


if __name__ == '__main__':
    app.run(debug=True)
