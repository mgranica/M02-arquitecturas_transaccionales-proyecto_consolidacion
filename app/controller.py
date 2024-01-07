from imagekitio import ImageKit
from flask import current_app
import requests
import base64
import os
from typing import Dict
from functools import wraps

from . import models


def set_api_connection(api="imagekit"):
    credentials = current_app.credentials[api]
    # Set API connection credentials
    imagekit = ImageKit(
        public_key=credentials["public_key"],
        private_key=credentials["private_key"],
        url_endpoint=credentials["url_endpoint"],
    )
    return imagekit


def exception_handler(error_description):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the exception and re-raise it for further handling
                raise Exception(f"{error_description}: {str(e)}")

        return wrapper

    return decorator


@exception_handler("Error uploading public URL")
def upload_public_url(img_b64, file_name="my_file_name.jpg"):
    # Set API connection credentials
    imagekit = set_api_connection()
    # upload image
    upload_info = imagekit.upload(file=img_b64, file_name=file_name)

    return {
        "url": upload_info.url,
        "id": upload_info.file_id,
        "path": upload_info.file_path,
        "size": upload_info.size,
    }


@exception_handler("Error deleting public URL")
def delete_public_url(file_id: str):
    # Set API connection credentials
    imagekit = set_api_connection()
    # delete an image
    result = imagekit.delete_file(file_id=file_id)

    return result


def decode_image(encoded_data):
    # Decode the base64-encoded string
    return base64.b64decode(encoded_data)


@exception_handler("Error saving Image")
def save_image(decoded_data, file_name, extension=".jpg"):
    result_path = os.environ.get("RESULT_PATH", "../static/results")
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    save_path = os.path.join(result_path, file_name + extension)
    # Save the decoded binary data as a .jpg file
    with open(save_path, mode="wb") as decoded_img:
        decoded_img.write(decoded_data)
    print(f"Image saved to {save_path}")
    return decoded_data


@exception_handler("Error during tags extraction")
def extract_tags(image_url: str, min_confidence: int, api="imagga"):
    try:
        credentials = current_app.credentials[api]

        if (
            not credentials
            or not credentials.get("api_key")
            or not credentials.get("api_secret")
        ):
            raise Exception("Invalid or missing Imagga API credentials")

        response = requests.get(
            f"https://api.imagga.com/v2/tags?image_url={image_url}",
            auth=(credentials["api_key"], credentials["api_secret"]),
        )
        tags = [
            {"tag": t["tag"]["en"], "confidence": t["confidence"]}
            for t in response.json()["result"]["tags"]
            if t["confidence"] > min_confidence
        ]
        return tags
    except Exception as e:
        raise Exception(f"Imagga API connection error: {str(e)}")


@exception_handler("Error inserting records in Pictures table")
def insert_pictures(file_id, file_path, size, date):
    models.insert_pictures_values(file_id, file_path, size, date)


@exception_handler("Error inserting records in Tags table")
def insert_tags(file_id, tags, date):
    models.insert_tags_values(file_id, tags, date)


@exception_handler("Query images Error")
def get_images(min_date=None, max_date=None, tags=None):
    # Get result
    result = models.select_images(min_date, max_date, tags)
    if not result:
        raise Exception(f"No Images were collected with the tags: {tags}")
    # Format response
    columns = result.keys()
    response = [
        {
            **{
                key: value
                for key, value in i.items()
                if key not in ["tags", "confidences"]
            },
            "tags": {
                key: value for key, value in i.items() if key in ["tags", "confidences"]
            },
        }
        for i in [dict(zip(columns, row)) for row in result]
    ]
    return response


@exception_handler("Query image Error")
def get_image(picture_id):
    # Get result
    result = models.select_image(picture_id)
    if not result:
        raise Exception(f"{picture_id} no included in the DB")
    # Format response
    columns = result.keys()
    response = [
        {
            **{
                key: value
                for key, value in i.items()
                if key not in ["tags", "confidences"]
            },
            "tags": {
                key: value for key, value in i.items() if key in ["tags", "confidences"]
            },
        }
        for i in [dict(zip(columns, row)) for row in result]
    ]
    return response


@exception_handler("Query tags Error")
def get_tags(min_date=None, max_date=None):
    # Get result
    result = models.select_tags(min_date, max_date)
    if not result:
        raise Exception(f"No tags were generated within those dates")
    # Format Response
    columns = result.keys()
    response = [dict(zip(columns, row)) for row in result]
    return response
