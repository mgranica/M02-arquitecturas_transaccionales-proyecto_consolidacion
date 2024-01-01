from flask import Blueprint, request, make_response
from . import controller
import os
import datetime

bp = Blueprint('images', __name__, url_prefix='/')


@bp.post("/images")
def post_image():
    
    encoded_data = request.json.get("data")
    min_confidence = request.json.get("min_confidence", 80)
    date = str(datetime.datetime.now())

    # generate public URL
    upload_info = controller.upload_public_url(encoded_data)
    # Tag extraction from public URL image
    tags = controller.extract_tags(upload_info["url"], min_confidence)
    # delete public URL image
    delete_img = controller.delete_public_url(upload_info["id"])
    # decode data
    decoded_data = controller.decode_image(encoded_data)
    # Store image
    controller.save_image(decoded_data, upload_info["id"])
    # insert into Pictures Table
    controller.insert_pictures(
        upload_info["id"], upload_info["path"], upload_info["size"], date
    )
    # insert into Tags Table
    controller.insert_tags(
        upload_info["id"], tags, date
    )

    return {
        "id": upload_info["id"],
        "size": upload_info["size"],
        "date": date,
        "tags": tags,
        #"data": decoded_data
    }


@bp.get("/images")
def get_images():
    min_date = request.args.get("min_date", None)
    max_date = request.args.get("max_date", None)
    tags = request.args.get("tags", None)
    
    # select images
    response = controller.get_images(min_date, max_date , tags)
    
    return response


@bp.get("/images/<picture_id>")
def get_image(picture_id):
    
    # select images
    response = controller.get_image(picture_id)
    
    return response


@bp.get("/tags")
def get_tags():    
    min_date = request.args.get("min_date", None)
    max_date = request.args.get("max_date", None)
    
    # select images
    response = controller.get_tags(min_date, max_date)
    
    return response