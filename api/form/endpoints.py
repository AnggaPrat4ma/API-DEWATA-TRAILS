"""Routes for module form"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

form_endpoints = Blueprint('form', __name__)
UPLOAD_FOLDER = "img"


@form_endpoints.route('/read', methods=['GET'])
#   @jwt_required()
def read():
    """Routes for module get list form"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM form_orders"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200


@form_endpoints.route('/create', methods=['POST'])
#@jwt_required()
def create():
    """Routes for module create an order"""
    required = get_form_data(["full_name", "id_user", "id_paket", "jumlah", "alamat", "id_jenis"])
    full_name = required["full_name"]
    id_user = required["id_user"]
    id_paket = required["id_paket"]
    jumlah = required["jumlah"]
    alamat = required["alamat"]
    id_jenis = required["id_jenis"]

    uploaded_file = request.files.get('gambar')
    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({"err_message": "No file uploaded"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO form_orders (full_name, id_user, id_paket, jumlah, alamat, gambar, id_jenis)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    request_insert = (full_name, id_user, id_paket, jumlah, alamat, file_path, id_jenis)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"message": "Inserted", "id_order": new_id}), 201
    return jsonify({"message": "Cannot insert data"}), 500


@form_endpoints.route('/delete/<id_order>', methods=['DELETE'])
@jwt_required()
def delete(id_order):
    """Routes for module delete an order"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM form_orders WHERE id_order = %s"
    delete_id = (id_order,)
    cursor.execute(delete_query, delete_id)
    if cursor.rowcount <= 0:
        return jsonify({"err_message": "Data not deleted"}), 400
    connection.commit()
    cursor.close()

    return jsonify({"message": "Deleted", "id_order": id_order}), 200


@form_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "OK", "data": "Uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Cannot upload file"}), 400


@form_endpoints.route('/update/<int:id_order>', methods=['PUT'])
def update(id_order):
    """Routes for module update a booking"""
    # Mengambil data dari FormData
    status = request.form.get("status")  # Gunakan .get() untuk menangani key yang tidak ada
    print(f"Booking ID: {id_order}, Status: {status}")

    if not status:
        return jsonify({"error": "Status is required"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE form_orders
    SET status=%s
    WHERE id_order=%s
    """
    cursor.execute(update_query, (status, id_order))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Booking updated", "id_order": id_order}), 200


@form_endpoints.route('/read/<int:id_user>', methods=['GET'])
def read_by_user(id_user):
    """Routes for module get list form by user id"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    select_query = "SELECT * FROM form_orders WHERE id_user = %s"
    cursor.execute(select_query, (id_user,))
    results = cursor.fetchall()
    cursor.close()

    if results:
        return jsonify({"message": "OK", "datas": results}), 200
    return jsonify({"message": "No data found for this user"}), 404
 
