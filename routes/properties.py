from flask import Blueprint, jsonify

from utils import io



bp_properties = Blueprint('properties', __name__)




@bp_properties.route('/api/v1/properties', methods=['GET'])
def api_agent():
    return jsonify(io.load_json("data/properties.json"))



@bp_properties.route('/properties', methods=['GET'])
def api_agent():
    return io.load_json("data/properties.json")['x_super']



