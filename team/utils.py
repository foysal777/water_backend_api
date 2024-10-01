import requests

def upload_image_to_imgbb(image_file):
    imgbb_api_key = 'add07eb16060304e9d624f9962001708'  # Replace with your actual imgbb API key
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": imgbb_api_key,
        "image": image_file,
    }
    response = requests.post(url, data=payload)
    response_data = response.json()

    if response.status_code == 200 and response_data['status'] == 200:
        return response_data['data']['url']
    else:
        return None
