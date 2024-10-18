import requests
from django.core.files.base import ContentFile
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content, name="avatar.png")
    return None


