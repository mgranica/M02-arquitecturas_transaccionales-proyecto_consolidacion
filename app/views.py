from flask import Blueprint, request, make_response, jsonify
from . import controller
import os
from datetime import datetime

bp = Blueprint("images", __name__, url_prefix="/")


def validate_json_data(request_json):
    if not request_json or "data" not in request_json:
        raise ValueError("Missing 'data' parameter in the request body")


def validate_min_confidence(min_confidence_str):
    try:
        min_confidence = int(min_confidence_str)
        if not (0 <= min_confidence <= 100):
            raise ValueError("Value must be between 0 and 100")
    except ValueError:
        raise ValueError("'min_confidence' must be a valid integer between 0 and 100")


def validate_datetime_format(date_str, datetime_format="%Y-%m-%d %H:%M:%S"):
    ## TODO: redefine date format
    try:
        datetime.strptime(date_str, datetime_format)
    except ValueError:
        raise ValueError("Invalid 'date' format. Use YYYY-MM-DD HH:MM:SS.")


@bp.post("/images")
def post_image():
    try:
        request_json = request.json
        validate_json_data(request_json)

        encoded_data = request_json.get("data")

        min_confidence_str = request.args.get("min_confidence", "80")
        validate_min_confidence(min_confidence_str)

        date = str(datetime.now())

        # generate public URL
        upload_info = controller.upload_public_url(encoded_data)
        # Tag extraction from public URL image
        tags = controller.extract_tags(upload_info["url"], int(min_confidence_str))
        # delete public URL image
        delete_img = controller.delete_public_url(upload_info["id"])
        # decode data
        decoded_data = controller.decode_image(encoded_data)
        # Save image
        save_path = controller.save_image(decoded_data, upload_info["id"])
        # insert into Pictures Table
        controller.insert_pictures(
            upload_info["id"], save_path, upload_info["size"], date
        )
        # insert into Tags Table
        controller.insert_tags(upload_info["id"], tags, date)

        return {
            "id": upload_info["id"],
            "size": upload_info["size"],
            "date": date,
            "tags": tags,
            "data": encoded_data,
        }
    except ValueError as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response


@bp.get("/images")
def get_images():
    try:
        min_date = request.args.get("min_date", None)
        max_date = request.args.get("max_date", None)
        tags = request.args.get("tags", None)

        if not (min_date == None):
            validate_datetime_format(min_date)

        if not (max_date == None):
            validate_datetime_format(max_date)

        # Split str & Remove spaces from each item in the list
        tags_list = [item.strip() for item in tags.split(",")]

        # select images
        response = controller.get_images(min_date, max_date, tags_list)

        return response

    except ValueError as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response


@bp.get("/images/<picture_id>")
def get_image(picture_id):
    try:
        # Call controller to get the image
        response = controller.get_image(picture_id)

        return response

    except ValueError as value_error:
        response = make_response(
            jsonify({"error": f"Invalid picture_id: {str(value_error)}"}), 400
        )
        return response

    except Exception as e:
        response = make_response(
            jsonify({"error": f"Image with ID {picture_id} not found"}), 404
        )
        return response


@bp.get("/tags")
def get_tags():
    try:
        min_date = request.args.get("min_date", None)
        max_date = request.args.get("max_date", None)
        if not (min_date == None):
            validate_datetime_format(min_date)

        if not (max_date == None):
            validate_datetime_format(max_date)

        # select images
        response = controller.get_tags(min_date, max_date)

        return response
    except ValueError as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 400)
        return response
