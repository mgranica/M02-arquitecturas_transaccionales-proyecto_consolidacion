
from imagekitio import ImageKit
import requests
import base64
import json
import os
from typing import Dict

from . import models


def get_credentials():
    credentials_path = os.environ.get("CREDENTIAL_PATH", "./credentials.json")
    # Load credentials from the JSON file
    with open(credentials_path, 'r') as file:
        credentials = json.load(file)
    return credentials

def encode_image(image_path):
    with open(image_path, mode="rb") as img:
        img_b64 = base64.b64encode(img.read())
    return img_b64

def set_api_connection(credentials):
    # Set API connection credentials
    imagekit = ImageKit(
        public_key=credentials["public_key"],
        private_key=credentials["private_key"],
        url_endpoint =credentials["url_endpoint"]
    )
    return imagekit

def upload_public_url(img_b64, credentials: Dict[str,str], file_name="my_file_name.jpg"):
    # Set API connection credentials
    imagekit = set_api_connection(credentials)
    # upload image
    upload_info = imagekit.upload(file=img_b64, file_name=file_name)
    
    return {
        "url": upload_info.url,
        "id": upload_info.file_id,
        "path":  upload_info.file_path,
        "size": upload_info.size
    }

def delete_public_url(credentials: Dict[str,str], file_id: str):
    # Set API connection credentials
    imagekit = set_api_connection(credentials)
    # delete an image
    result = imagekit.delete_file(file_id=file_id)
    
    return result

def decode_and_save_image(encoded_data, file_name, extension=".jpg"):
    result_path = os.environ.get("RESULT_PATH", "../static/results")

    save_path = os.path.join(result_path, file_name + extension)
    print(save_path)
    try:
        # Decode the base64-encoded string
        decoded_data = base64.b64decode(encoded_data)

        # Save the decoded binary data as a .jpg file
        with open(save_path, mode="wb") as decoded_img:
            decoded_img.write(decoded_data)

        print(f"Image saved to {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def extract_tags(image_url: str, credentials: Dict[str,str], min_confidence: int):
    response = requests.get(
            f"https://api.imagga.com/v2/tags?image_url={image_url}", 
            auth=(
                credentials["api_key"], credentials["api_secret"]
            )
    )
    tags = [
        {
            "tag": t["tag"]["en"],
            "confidence": t["confidence"]
        }
        for t in response.json()["result"]["tags"]
        if t["confidence"] > min_confidence
    ]
    return tags

def insert_pictures(file_id, file_path, size, date):
    models.insert_pictures_values(file_id, file_path, size, date)
  
def insert_tags(file_id, tags, date):
    models.insert_tags_values(file_id, tags, date)

def get_images(min_date=None, max_date=None , tags=None):
    # Get result
    result = models.select_images(min_date, max_date ,tags)
    # Format response
    columns = result.keys()
    response = [
        {**{key: value for key, value in i.items() if key not in ["tags", "confidences"]},
         "tags": {key: value for key, value in i.items() if key in ["tags", "confidences"]}}
        for i in [ 
            dict(zip(columns, row)) for row in result
        ]
    ]
    return response

def get_image(picture_id):
    # Get result
    result = models.select_image(picture_id)
    # Format response
    columns = result.keys()
    response = [
        {**{key: value for key, value in i.items() if key not in ["tags", "confidences"]},
         "tags": {key: value for key, value in i.items() if key in ["tags", "confidences"]}}
        for i in [ 
            dict(zip(columns, row)) for row in result
        ]
    ]
    return response
   
def get_tags(min_date=None, max_date=None):
    # Get result
    result = models.select_tags(min_date, max_date)
    # Format Response
    columns = result.keys()
    response = [
        dict(zip(columns, row))
        for row in result
    ]
    return response
