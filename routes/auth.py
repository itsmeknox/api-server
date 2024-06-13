from flask import request, jsonify, Blueprint

from modules.constants import ServerConfig

from modules.helpers import (
    validate_license
)

from modules.encryption import (
    CryptoUtils,
    EncryptionUtils,
    JwtUtils
)
import time
import json


bp_auth = Blueprint('auth', __name__)

constants = ServerConfig()

class LevelOne:
    def __init__(self, encrypted_data, secret):
        self.encrypted_data = encrypted_data
        self.license = secret
            


    def process_request(self):
        try:
            self.data = CryptoUtils.decrypt_with_private_key(
                self.encrypted_data, constants.PRIVATE_KEY_1)
        except Exception:
            return jsonify({"error": "Unauthorized", "message": "Invalid Encryption"}), 400

        try:
            self.json_data = json.loads(self.data)
        except Exception:
            return jsonify({"error": "InvalidJsonFormat", "message": "Invalid Json Format"}), 400

        try:
            run_time_key = self.json_data["run_time_key"]
            license_key = CryptoUtils.decrypt_with_private_key(self.license, constants.PRIVATE_KEY_1)
            session_id = self.json_data["session_id"]
            time_stamp = self.json_data["timestamp"]
        except KeyError:
            return jsonify({"error": "InvalidData", "message": "Key Values Missing"}), 400

        if not validate_license(run_time_key, license_key):
            return jsonify({"error": "InvalidLicense"}), 401

        payload = json.dumps({
            "success": True,
            "license": license_key,
            "session_id": session_id,
            "timestamp": time.time(),
            "master_key": constants.MASTER_KEY_1,
            "message": "The license is valid",
            "session_token": JwtUtils.encrypt_jwt({
                "session_id": session_id,
                "timestamp": time.time(),
            },
                constants.JWT_SECRET_1,
                expire_seconds=900
            )
        })

        # Encrypting Bottom with Run Time Key
        encrypted_payload_bottom = EncryptionUtils.encrypt_message(payload, run_time_key)

        # Encrypting Top with HC Encryption Key
        encrypted_payload_top = EncryptionUtils.encrypt_message(
            encrypted_payload_bottom, constants.HC_ENCRYPTION_KEY)

        # Generating Signature 1 for top
        signature = CryptoUtils.generate_signature(encrypted_payload_top, constants.PRIVATE_KEY_1)
            

        signature_2 = CryptoUtils.generate_signature(
            payload, constants.PRIVATE_KEY_1)
        headers = {
            "signature": signature,
            "signature_2": signature_2
        }
        return jsonify({"data": encrypted_payload_top}), 200, headers


@bp_auth.route("/authenticate", methods=["POST"])
def index():
    if not request.is_json or "data" not in request.get_json() or "secret" not in request.get_json():
        return jsonify({"error": "Invalid Json Request Body"}), 400
    json_data = request.get_json()

    try:
        return LevelOne(json_data['data'], secret=json_data['secret']).process_request()
    except Exception as e:
        return jsonify({"error": "InternalServerError", "message": "An error occured while processing the request. Please try again."}), 500

