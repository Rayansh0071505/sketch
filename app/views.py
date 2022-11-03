from flask import Flask, render_template, request
import os
from app import app
from PIL import Image

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['GENERATED_FILE'] = 'app/static/generated'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        import cv2
        
        file_upload = request.files['file_upload']
        filename = file_upload.filename
        
        uploaded_image = Image.open(file_upload)
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))
        
        uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

        cv2.imshow('carss', uploaded_image)

        # get image height and width
        height, width, channels = uploaded_image.shape

        img_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
        img_blend = cv2.divide(img_gray, img_blur, scale=256)
        cv2.imshow('cars Pencil Sketch', img_blend)

        # save image using opencv
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), img_blend)

        sketch =  'static/uploads/image.jpg'
        original =  'static/generated/image_diff.jpg'
        return render_template('index.html',sketch=sketch,original=original)


if __name__ == '__main__':
    app.run(debug=True)
