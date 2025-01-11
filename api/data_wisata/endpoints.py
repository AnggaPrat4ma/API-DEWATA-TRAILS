"""Routes for module wisata"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

wisata_endpoints = Blueprint('wisata', __name__)

@wisata_endpoints.route('/read', methods=['GET'])
#@jwt_required()
def read():
    """Routes for module get list wisata"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM data_wisata"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()  # Close the cursor after query execution
    return jsonify({"message": "OK", "datas": results}), 200

@wisata_endpoints.route('/create', methods=['POST'])
#@jwt_required()
def create():
    """Routes for module create a wisata"""
    # Ambil data dari form
    required = get_form_data(["nama_wisata", "deskripsi", "rating_wisata", "video", "gambar", "id_paket"])
    nama_wisata = required["nama_wisata"]
    deskripsi = required["deskripsi"]
    rating_wisata = required["rating_wisata"]
    video = required["video"]  # Video adalah link, bukan file
    gambar = required["gambar"]  # Gambar adalah link (thumbnail)
    id_paket = required["id_paket"]  # ID Paket dari data_paket

    connection = get_connection()
    cursor = connection.cursor()

    # Periksa apakah id_paket yang diberikan tersedia dalam tabel data_paket
    check_paket_query = "SELECT COUNT(*) FROM travel WHERE id_paket = %s"
    cursor.execute(check_paket_query, (id_paket,))
    paket_exists = cursor.fetchone()[0]

    if not paket_exists:
        cursor.close()
        connection.close()
        return jsonify({"message": "Invalid id_paket. Paket tidak ditemukan"}), 400

    # Masukkan data ke tabel data_wisata
    insert_query = """
        INSERT INTO data_wisata (nama_wisata, deskripsi, gambar, video, rating_wisata, id_paket) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    request_insert = (nama_wisata, deskripsi, gambar, video, rating_wisata, id_paket)
    cursor.execute(insert_query, request_insert)
    connection.commit()  # Commit perubahan ke database
    new_id = cursor.lastrowid  # Ambil ID wisata yang baru ditambahkan
    cursor.close()
    connection.close()

    if new_id:
        return jsonify({"nama_wisata": nama_wisata, "message": "Inserted", "id_wisata": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500


@wisata_endpoints.route('/update/<id_wisata>', methods=['PUT'])
#@jwt_required()
def update(id_wisata):
    """Routes for module update a wisata"""
    required = get_form_data(["nama_wisata", "deskripsi", "rating_wisata", "video", "gambar", "id_paket"])
    nama_wisata = required["nama_wisata"]
    deskripsi = required["deskripsi"]
    rating_wisata = required["rating_wisata"]
    video = required["video"]  # Video is a link, not a file
    gambar = required["gambar"]  # Gambar is now a link (thumbnail)
    id_paket = required["id_paket"]

    connection = get_connection()
    cursor = connection.cursor()

    # Periksa apakah id_paket yang diberikan tersedia dalam tabel data_paket
    check_paket_query = "SELECT COUNT(*) FROM travel WHERE id_paket = %s"
    cursor.execute(check_paket_query, (id_paket,))
    paket_exists = cursor.fetchone()[0]

    if not paket_exists:
        cursor.close()
        connection.close()
        return jsonify({"message": "Invalid id_paket. Paket tidak ditemukan"}), 400

    update_query = """
        UPDATE data_wisata 
        SET nama_wisata=%s, deskripsi=%s, gambar=%s, video=%s, rating_wisata=%s, id_paket=%s 
        WHERE id_wisata=%s
    """
    update_request = (nama_wisata, deskripsi, gambar, video, rating_wisata, id_paket, id_wisata)
    cursor.execute(update_query, update_request)
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data Not Updated"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    data = {"message": "Updated", "id_wisata": id_wisata}
    return jsonify(data), 200

@wisata_endpoints.route('/delete/<id_wisata>', methods=['DELETE'])
#@jwt_required()
def delete(id_wisata):
    """Routes for module to delete a wisata"""
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM data_wisata WHERE id_wisata = %s"
    delete_id = (id_wisata,)
    cursor.execute(delete_query, delete_id)
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data Not Deleted"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    data = {"message": "Data deleted", "id_wisata": id_wisata}
    return jsonify(data)

@wisata_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Routes for upload file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join("img", uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "OK", "data": "Uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't upload data"}), 400


@wisata_endpoints.route('/read_by_paket/<id_paket>', methods=['GET'])
#@jwt_required()
def read_by_paket(id_paket):
    """Routes for fetching wisata data by id_paket"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM data_wisata WHERE id_paket = %s"
    cursor.execute(select_query, (id_paket,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if results:
        return jsonify({"message": "OK", "datas": results}), 200
    return jsonify({"message": "No data found for the given id_paket"}), 404
