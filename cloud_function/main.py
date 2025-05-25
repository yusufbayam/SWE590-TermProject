from flask import request, make_response
from PIL import Image, ImageOps
import io
import traceback
import os

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

def negative_image(request):
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        return add_cors_headers(response)

    if request.method != 'POST':
        response = make_response('POST method required', 405)
        return add_cors_headers(response)

    if 'file' not in request.files:
        response = make_response('No file part', 400)
        return add_cors_headers(response)

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
        return add_cors_headers(response)
    except Exception as e:
        print(traceback.format_exc())
        response = make_response(str(e), 500)
        return add_cors_headers(response)