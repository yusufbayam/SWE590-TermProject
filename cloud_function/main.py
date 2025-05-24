from flask import request, make_response
from PIL import Image, ImageOps
import io
import traceback

def negative_image(request):
    if request.method != 'POST':
        return make_response('POST method required', 405)

    if 'file' not in request.files:
        return make_response('No file part', 400)

    file = request.files['file']
    try:
        img = Image.open(file.stream)
        inverted_image = ImageOps.invert(img.convert('RGB'))
        img_byte_arr = io.BytesIO()
        inverted_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        response = make_response(img_byte_arr.read())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='negative.png')
        return response
    except Exception as e:
        print(traceback.format_exc())
        return make_response(str(e), 500)