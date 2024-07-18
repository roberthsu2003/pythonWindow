import requests
from io import BytesIO

def get_image(url):
    response = requests.get(url)
    # 取得HTML狀態碼
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Error loading image")

def decode_image(image_content):
    return BytesIO(image_content)
