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


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Post listing, user has option to sort by title or content"""

    sort_arg = request.args.get('sort', '').strip().lower()
    sort_direction = request.args.get('direction', 'asc').strip().lower()

    if sort_arg and sort_arg not in ['title', 'content']:
        return jsonify({"error": "Invalid sort input. Use 'title' or 'content' instead!"}), 400
    if sort_direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort direction. Use 'asc' or 'desc' instead!"}), 400

    returned_posts = POSTS[:]

    # If user wishes, sort
    if sort_arg:
        reverse = sort_direction == 'desc'
        returned_posts.sort(key=lambda x: x[sort_arg].lower(), reverse=reverse)

    return jsonify(returned_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add Endpoint"""
    data = request.get_json()

    # Error handling part for title and content + strip for cleanup
    if not data:
        return jsonify({"error": "Request must be json"}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title:
        return jsonify({"error": "Title is a required field"}), 400
    if not content:
        return jsonify({"error": "Content is a required field"}), 400

    # ID generation process
    new_post = {
        "id": new_id_gen(),
        "title": title,
        "content": content
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)