from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Masterblog API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

id_stat = len(POSTS) + 1

def new_id_gen():
    """Generates a unique id using our global id counter 'id_stat' """
    global id_stat
    new_id = id_stat
    id_stat += 1
    return new_id

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)