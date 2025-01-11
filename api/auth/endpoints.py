import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from helper.db_helper import get_connection

bcrypt = Bcrypt()
auth_endpoints = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'img'  # Ganti dengan folder upload yang diinginkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Ekstensi file yang diizinkan
# Pastikan folder upload ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_endpoints.route('/login', methods=['POST'])
def login():
    """Routes for authentication"""
    
    # Ambil data username dan password dari form request
    email = request.form.get('email')
    password = request.form.get('password')

    # Validasi jika email atau password kosong
    if not email or not password:
        return jsonify({"msg": "email and password are required"}), 400

    # Menggunakan try-finally untuk memastikan cursor dan koneksi ditutup
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True, buffered=True)  # Gunakan buffered=True untuk menghindari error Unread result found
        
        # Query untuk mengambil data user berdasarkan email
        query = "SELECT * FROM akun WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"msg": "Bad email or password"}), 401

        # Memeriksa password yang dimasukkan dengan password yang tersimpan di database
        if not bcrypt.check_password_hash(user['password'], password):
            return jsonify({"msg": "Bad email or password"}), 401
        
        # Membuat token akses
        access_token = create_access_token(
            identity={'id_user': user['id_user']},
            additional_claims={'roles': user.get('role', 'user')}  # Menambahkan roles ke dalam claims
        )
        
        decoded_token = decode_token(access_token)
        expires = decoded_token['exp']

        return jsonify({
            "access_token": access_token,
            "expires_in": expires,
            "type": "Bearer"
        })
    
    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500
    
    finally:
        # Menutup cursor dan koneksi setelah operasi selesai
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@auth_endpoints.route('/register', methods=['POST'])
def register():
    """Routes for register"""
    nama_user = request.form['nama_user']
    email = request.form['email']
    password = request.form['password']
    role = request.form.get('role', 'user')  # Default role is 'user'

    if not nama_user or not email or not password:
        return jsonify({"msg": "All fields (nama_user, email, password) are required"}), 400

    # Handle file upload
    if 'images' not in request.files:
        return jsonify({"msg": "Image file is required"}), 400

    file = request.files['images']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"msg": "Invalid file type. Allowed types are png, jpg, jpeg, gif"}), 400

    # Secure the filename and save it
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # To hash a password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO akun (nama_user, email, password, role, images) VALUES (%s, %s, %s, %s, %s)"
    request_insert = (nama_user, email, hashed_password, role, file_path)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"message": "OK",
                        "description": "User created",
                        "id_user": new_id,
                        "email": email,
                        "nama_user": nama_user,
                        "role": role,
                        "images": file_path}), 201

    return jsonify({"message": "Failed, cannot register user"}), 501

