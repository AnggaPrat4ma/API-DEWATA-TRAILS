"""Routes for module berita"""
import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from flask_jwt_extended import jwt_required

berita_endpoints = Blueprint('berita', __name__)
UPLOAD_FOLDER = "img"

@berita_endpoints.route('/read', methods=['GET'])
#@jwt_required()
def read():
    """Routes for getting a list of berita"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM berita"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200


@berita_endpoints.route('/create', methods=['POST'])
#@jwt_required()
def create():
    """Routes for creating a berita item"""
    required = get_form_data(["judul", "deskripsi", "source"])
    judul = required["judul"]
    deskripsi = required["deskripsi"]
    source = required["source"]

    # Handle image upload
    if 'image' not in request.files:
        return jsonify({"err_message": "Image is required"}), 400

    uploaded_file = request.files['image']
    if uploaded_file.filename == '':
        return jsonify({"err_message": "Invalid file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO berita (judul, deskripsi, image, source) VALUES (%s, %s, %s, %s)"
    request_insert = (judul, deskripsi, file_path, source)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    if new_id:
        return jsonify({"message": "Inserted", "id_berita": new_id}), 201
    return jsonify({"message": "Cannot Insert Data"}), 500


@berita_endpoints.route('/update/<int:id_berita>', methods=['PUT'])
#@jwt_required()
def update(id_berita):
    """Routes for updating a berita item"""
    judul = request.form.get('judul')
    deskripsi = request.form.get('deskripsi')
    source = request.form.get('source')

    if not (judul and deskripsi and source):
        return jsonify({"err_message": "All fields are required"}), 400

    # Handle optional image update
    image_path = None
    if 'image' in request.files:
        uploaded_file = request.files['image']
        if uploaded_file.filename != '':
            image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(image_path)

    connection = get_connection()
    cursor = connection.cursor()

    if image_path:
        update_query = "UPDATE berita SET judul=%s, deskripsi=%s, image=%s, source=%s WHERE id_berita=%s"
        update_request = (judul, deskripsi, image_path, source, id_berita)
    else:
        update_query = "UPDATE berita SET judul=%s, deskripsi=%s, source=%s WHERE id_berita=%s"
        update_request = (judul, deskripsi, source, id_berita)

    cursor.execute(update_query, update_request)
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data Not Updated"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Updated", "id_berita": id_berita}), 200


@berita_endpoints.route('/delete/<int:id_berita>', methods=['DELETE'])
#@jwt_required()
def delete(id_berita):
    """Routes for deleting a berita item"""
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM berita WHERE id_berita = %s"
    cursor.execute(delete_query, (id_berita,))
    if cursor.rowcount <= 0:
        cursor.close()
        connection.close()
        return jsonify({"err_message": "Data Not Deleted"}), 400

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Data Deleted", "id_berita": id_berita}), 200


@berita_endpoints.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """Routes for uploading an image file"""
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "File Uploaded", "file_path": file_path}), 200
    return jsonify({"err_message": "Can't Upload File"}), 400

@berita_endpoints.route('/read/<int:id_berita>', methods=['GET'])
#@jwt_required()
def read_by_id(id_berita):
    """Routes for getting a berita item by id"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Query to get berita by ID
    select_query = "SELECT * FROM berita WHERE id_berita = %s"
    cursor.execute(select_query, (id_berita,))
    result = cursor.fetchone()  # Use fetchone to get a single row
    
    cursor.close()
    connection.close()

    if result:
        return jsonify({"message": "OK", "data": result}), 200
    return jsonify({"err_message": "Berita not found"}), 404
