import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

paket_endpoints = Blueprint('travel', __name__)
UPLOAD_FOLDER = "img"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@paket_endpoints.route('/read', methods=['GET'])
#@jwt_required()
def read():
    """Route for getting list of paket"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM travel"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@paket_endpoints.route('/create', methods=['POST'])
#@jwt_required()
def create():
    """Route for creating a new paket"""
    nama_paket = request.form['nama_paket']
    deskripsi_pkt = request.form['deskripsi_pkt']
    rating_paket = request.form['rating_paket']

    if 'gambar' not in request.files:
        return jsonify({"err_message": "No file part in the request"}), 400

    gambar_file = request.files['gambar']
    if gambar_file.filename == '':
        return jsonify({"err_message": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, gambar_file.filename)
    gambar_file.save(file_path)

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = """INSERT INTO travel (nama_paket, deskripsi_pkt, gambar, rating_paket) \
                      VALUES (%s, %s, %s, %s)"""
    request_insert = (nama_paket, deskripsi_pkt, file_path, rating_paket)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()

    if new_id:
        return jsonify({"message": "Inserted", "id_paket": new_id}), 201
    return jsonify({"message": "Cannot insert data"}), 500


@paket_endpoints.route('/update/<int:id_paket>', methods=['PUT'])
#@jwt_required()
def update(id_paket):
    """Route for updating a paket"""
    nama_paket = request.form['nama_paket']
    deskripsi_pkt = request.form['deskripsi_pkt']
    rating_paket = request.form['rating_paket']

    file_path = None
    if 'gambar' in request.files:
        gambar_file = request.files['gambar']
        if gambar_file.filename != '':
            file_path = os.path.join(UPLOAD_FOLDER, gambar_file.filename)
            gambar_file.save(file_path)

    connection = get_connection()
    cursor = connection.cursor()

    if file_path:
        update_query = """UPDATE travel SET nama_paket=%s, deskripsi_pkt=%s, gambar=%s, rating_paket=%s \
                          WHERE id_paket=%s"""
        update_request = (nama_paket, deskripsi_pkt, file_path, rating_paket, id_paket)
    else:
        update_query = """UPDATE travel SET nama_paket=%s, deskripsi_pkt=%s, rating_paket=%s \
                          WHERE id_paket=%s"""
        update_request = (nama_paket, deskripsi_pkt, rating_paket, id_paket)

    cursor.execute(update_query, update_request)
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data not updated"}), 400
    
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Updated", "id_paket": id_paket}), 200


@paket_endpoints.route('/delete/<int:id_paket>', methods=['DELETE'])
#@jwt_required()
def delete(id_paket):
    """Route for deleting a paket"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM travel WHERE id_paket = %s"
    cursor.execute(delete_query, (id_paket,))
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data not deleted"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Data deleted", "id_paket": id_paket}), 200


@paket_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Route for uploading a file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    return jsonify({"err_message": "Cannot upload file"}), 400


@paket_endpoints.route('/read/<int:id_paket>', methods=['GET'])
#@jwt_required()
def read_by_id(id_paket):
    """Route for getting a specific travel data by id_paket"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query untuk mendapatkan data berdasarkan id_paket
    select_query = "SELECT * FROM travel WHERE id_paket = %s"
    cursor.execute(select_query, (id_paket,))
    result = cursor.fetchone()  # Ambil hanya satu data
    cursor.close()
    connection.close()
    
    if not result:
        return jsonify({"message": "Data not found"}), 404

    return jsonify({"message": "OK", "data": result}), 200
