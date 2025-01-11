"""Small apps to demonstrate endpoints with basic feature - CRUD"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from api.books.endpoints import books_endpoints
from api.data_wisata.endpoints import wisata_endpoints
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints
from api.berita.endpoints import berita_endpoints
from api.travel.endpoints import paket_endpoints
from api.jenis.endpoints import jenis_endpoints
from api.form.endpoints import form_endpoints
from config import Config
from static.static_file_server import static_file_server

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

jwt.init_app(app)

# register the blueprint
app.register_blueprint(auth_endpoints, url_prefix='/api/auth')
app.register_blueprint(protected_endpoints,
                       url_prefix='/api/v1/protected')
app.register_blueprint(books_endpoints, url_prefix='/api/v1/books')
app.register_blueprint(wisata_endpoints, url_prefix='/api/wisata')
app.register_blueprint(berita_endpoints, url_prefix='/api/berita')
app.register_blueprint(paket_endpoints, url_prefix='/api/travel')
app.register_blueprint(form_endpoints, url_prefix='/api/form')
app.register_blueprint(jenis_endpoints, url_prefix='/api/jenis')
app.register_blueprint(static_file_server, url_prefix='/static/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
