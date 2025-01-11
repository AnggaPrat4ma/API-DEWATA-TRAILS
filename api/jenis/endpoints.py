import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

jenis_endpoints = Blueprint('jenis', __name__)
UPLOAD_FOLDER = "img"


@jenis_endpoints.route('/read', methods=['GET'])
#@jwt_required()
def read():
    """Route to get list of jenis"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM jenis"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200


@jenis_endpoints.route('/create', methods=['POST'])
#@jwt_required()
def create():
    """Route to create a new jenis"""
    required = get_form_data(["nama_jenis", "fasilitas", "price"])
    nama_jenis = required["nama_jenis"]
    fasilitas = required["fasilitas"]
    price = required["price"]

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO jenis (nama_jenis, fasilitas, price) VALUES (%s, %s, %s)"
    request_insert = (nama_jenis, fasilitas, price)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()

    if new_id:
        return jsonify({"message": "Inserted", "id_jenis": new_id, "nama_jenis": nama_jenis}), 201
    return jsonify({"message": "Failed to insert data"}), 500


@jenis_endpoints.route('/update/<id_jenis>', methods=['PUT'])
#@jwt_required()
def update(id_jenis):
    """Route to update an existing jenis"""
    nama_jenis = request.form['nama_jenis']
    fasilitas = request.form['fasilitas']
    price = request.form['price']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE jenis SET nama_jenis=%s, fasilitas=%s, price=%s WHERE id_jenis=%s"
    update_request = (nama_jenis, fasilitas, price, id_jenis)
    cursor.execute(update_query, update_request)

    if cursor.rowcount <= 0:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"message": "Failed to update data"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Updated", "id_jenis": id_jenis}), 200


@jenis_endpoints.route('/delete/<id_jenis>', methods=['DELETE'])
#@jwt_required()
def delete(id_jenis):
    """Route to delete an existing jenis"""
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM jenis WHERE id_jenis = %s"
    cursor.execute(delete_query, (id_jenis,))

    if cursor.rowcount <= 0:
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({"message": "Failed to delete data"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Deleted", "id_jenis": id_jenis}), 200


@jenis_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Route to upload a file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    return jsonify({"message": "Failed to upload file"}), 400
