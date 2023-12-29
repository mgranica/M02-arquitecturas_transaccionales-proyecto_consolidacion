from flask import Blueprint, request, make_response
from . import controller
from flask import current_app
import datetime

bp = Blueprint('convert', __name__, url_prefix='/')


@bp.post("/convert")
def post_image():

    credentials_path = "./credentials.json"
    
    image_path = request.json.get("image")
    min_confidence = request.json.get("min_confidence", 80)
    date = str(datetime.datetime.now())

    # Get credentials
    credentials = controller.get_credentials(credentials_path)
    # encode image
    img_b64 = controller.encode_image(image_path)
    # generate public URL
    upload_info = controller.upload_public_url(img_b64, credentials["imagekit"])
    # Tag extraction from public URL image
    tags = controller.extract_tags(upload_info["url"], credentials["imagga"], min_confidence)
    # delete public URL image
    # Store image
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
        #"data": img_b64
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