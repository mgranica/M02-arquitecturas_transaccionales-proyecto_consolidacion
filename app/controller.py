
from imagekitio import ImageKit
import requests
import base64
import json
from typing import Dict

import models


def create_sql_engine(
    host: str, database: str, user: str, password: str
):
    # create SQLalchemy engine
    return  models.create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

def get_credentials(credentials_path):
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

def delete_public_url(img_b64, credentials: Dict[str,str], file_id):
    # Set API connection credentials
    imagekit = set_api_connection(credentials)
    # delete an image
    delete = imagekit.delete_file(file_id=file_id)
    
    return delete

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

def insert_pictures(engine, file_id, file_path, size, date):
    models.insert_pictures_values(engine, file_id, file_path, size, date)
  
def insert_tags(engine, file_id, tags, date):
    models.insert_tags_values(engine, file_id, tags, date)

def get_images(engine, min_date=None, max_date=None , tags=None):
    # Get result
    result = models.select_images(engine, min_date, max_date ,tags)
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

def get_image(engine, picture_id):
    # Get result
    result = models.select_image(engine, picture_id)
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
   
def get_tags(engine, min_date=None, max_date=None):
    # Get result
    result = models.select_tags(engine, min_date, max_date)
    # Format Response
    columns = result.keys()
    response = [
        dict(zip(columns, row))
        for row in result
    ]
    return response
