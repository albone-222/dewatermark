import jwt
import time
import requests
import base64
from dotenv import dotenv_values


config = dotenv_values()

def delete_watermark(image):
    presecret_key = config['SECRET_KEY']
    secret_key = base64.b64decode(presecret_key)
    time_ = int(time.time() * 1000 + 3e5)
    encoded_jwt = jwt.encode({'sub': 'ignore', 'platform': 'web', 'exp': time_}, secret_key, algorithm='HS256')
    url = "https://be-prod-1.snapedit.app/api/object_removal/v5/erase_watermark"

    payload = {'zoom_factor': '2'}
    files={'original_preview_image': image}
    headers = {
    'Authorization': f'Bearer {encoded_jwt}',
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.json()['edited_image']['image']


image_path = 'watermark.jpg'
output_image_path = 'unwatermark.jpg'
bynary_image = ''
with open(image_path, 'rb') as img:
    bynary_image = img.read()

image = delete_watermark(bynary_image)
with open(output_image_path, 'wb') as img:
    img = img.write(base64.b64decode(image))

