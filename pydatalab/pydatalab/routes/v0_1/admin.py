from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_login import current_user

from pydatalab.config import CONFIG
from pydatalab.models.utils import UserRole
from pydatalab.mongo import flask_mongo
from pydatalab.permissions import get_default_permissions

admin = Blueprint("admins", __name__)


@admin.before_request
def check_authentication():
    if request.method == "OPTIONS":
        return

    if not current_user.is_authenticated and not CONFIG.TESTING:
        return (jsonify({"status": "error", "message": "No user authenticated: Unauthorized"}), 401)

    if not current_user.role == UserRole.ADMIN:
        return jsonify({"error": "Insufficient privileges"}), 403


@admin.route("/users")
def get_users():
    users = flask_mongo.db.users.aggregate(
        [
            {"$match": get_default_permissions(user_only=True)},
            {
                "$lookup": {
                    "from": "roles",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "role",
                }
            },
            {
                "$addFields": {
                    "role": {
                        "$cond": {
                            "if": {"$eq": [{"$size": "$role"}, 0]},
                            "then": "user",
                            "else": {"$arrayElemAt": ["$role.role", 0]},
                        }
                    }
                }
            },
        ]
    )

    return jsonify({"status": "success", "data": list(users)})


@admin.route("/roles/<user_id>", methods=["PATCH"])
def save_role(user_id):
    request_json = request.get_json()

    if request_json is not None:
        user_role = request_json

    existing_user = flask_mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not existing_user:
        return (jsonify({"status": "error", "message": "User not found."}), 404)

    existing_role = flask_mongo.db.roles.find_one({"_id": ObjectId(user_id)})

    if not existing_role:
        if not user_role:
            return (jsonify({"status": "error", "message": "Role not provided for new user."}), 400)

        new_user_role = {"_id": ObjectId(user_id), **user_role}
        flask_mongo.db.roles.insert_one(new_user_role)

        return (jsonify({"status": "success", "message": "New user's role created."}), 201)

    update_result = flask_mongo.db.roles.update_one({"_id": ObjectId(user_id)}, {"$set": user_role})

    if update_result.matched_count != 1:
        return (jsonify({"status": "error", "message": "Unable to update user."}), 400)

    if update_result.modified_count != 1:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "No update was performed",
                }
            ),
            200,
        )

    return (jsonify({"status": "success"}), 200)


@admin.route("/admin/settings")
def get_all_settings():
    settings = flask_mongo.db.settings.find()
    return jsonify({"status": "success", "data": list(settings)}), 200


@admin.route("/admin/new_setting", methods=["POST"])
def create_setting():
    request_json = request.get_json()

    if not request_json:
        return jsonify({"status": "error", "message": "Invalid request body."}), 400

    name = request_json.get("name")
    value = request_json.get("value")
    description = request_json.get("description")
    access_level = request_json.get("access_level")

    if not name or not value or not access_level:
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    existing_setting = flask_mongo.db.settings.find_one({"name": name})

    if existing_setting:
        return jsonify({"status": "error", "message": f"Setting '{name}' already exists."}), 409

    new_setting = {
        "name": name,
        "value": value,
        "description": description,
        "access_level": access_level,
    }

    try:
        result = flask_mongo.db.settings.insert_one(new_setting)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    if result.inserted_id:
        return jsonify({"status": "success", "message": "Setting created successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to create setting."}), 500


@admin.route("/admin/settings/<setting_id>", methods=["PATCH"])
def save_settings(setting_id):
    request_json = request.get_json()

    if request_json is not None:
        new_setting = {"value": request_json}

    existing_setting = flask_mongo.db.settings.find_one({"_id": ObjectId(setting_id)})

    if not existing_setting:
        return (jsonify({"status": "error", "message": "Setting not found."}), 404)

    update_setting = flask_mongo.db.settings.update_one(
        {"_id": ObjectId(setting_id)}, {"$set": new_setting}
    )

    if update_setting.matched_count != 1:
        return (jsonify({"status": "error", "message": "Unable to update setting."}), 400)

    if update_setting.modified_count != 1:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "No update was performed",
                }
            ),
            200,
        )

    return (jsonify({"status": "success"}), 200)


@admin.route("/admin/delete_setting/<setting_id>", methods=["DELETE"])
def delete_setting(setting_id):
    try:
        setting_object_id = ObjectId(setting_id)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid setting_id: {str(e)}"}), 400

    existing_setting = flask_mongo.db.settings.find_one({"_id": setting_object_id})

    if not existing_setting:
        return jsonify({"status": "error", "message": "Setting not found."}), 404

    try:
        delete_result = flask_mongo.db.settings.delete_one({"_id": setting_object_id})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to delete setting: {str(e)}"}), 500

    if delete_result.deleted_count == 1:
        return jsonify({"status": "success", "message": "Setting deleted successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to delete setting."}), 500
