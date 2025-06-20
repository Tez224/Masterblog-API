from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    # here go's the endpoint for adding a post
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content"}), 400

    new_post = {
        'id': POSTS[-1]['id'] + 1 if POSTS else 1,
        'title': data['title'],
        'content': data['content'],
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201  # 201 = Created


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Checks if id in POSTS id's
    found_post = next((post for post in POSTS if post['id'] == id), None)

    if not found_post:
        return jsonify({"error": "Post not found"}), 404
    else:
        POSTS.remove(found_post)
        return jsonify(found_post), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400
    if 'title' not in data and 'content' not in data:
        return jsonify({"error": "Missing input no title or content provided."}), 400

    find_post = next((post for post in POSTS if post['id'] == id), None)

    if not find_post:
        return jsonify({"error": "Post not found"}), 404

    if 'title' in data:
        find_post['title'] = data['title']
    if 'content' in data:
        find_post['content'] = data['content']

    return jsonify(find_post), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
