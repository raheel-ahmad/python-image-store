import requests

class ImageService:
    def __init__(self):
        pass
    def download_image(self, image_url):
        if image_url == None or image_url == '':
            return None
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        return response.content

