"""Routes for module protected endpoints"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection
from helper.jwt_helper import get_roles


protected_endpoints = Blueprint('data_protected', __name__)


@protected_endpoints.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    """
    Routes for demonstrate protected data endpoints, 
    need jwt to visit this endpoint
    """
    current_user = get_jwt_identity()
    
    id_user = current_user['id_user']

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM akun WHERE id_user = %s"
    cursor.execute(query, (id_user,))
    user = cursor.fetchone()
    roles = get_roles()
    return jsonify({"message": "OK",
                    "user_logged": user,
                    "roles": roles}), 200

