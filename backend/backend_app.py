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
    """
    endpoint for getting all posts
    :return: json with all posts
    """
    sort = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    valid_sort_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if sort and sort not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field: '{sort}'. Must be one of {list(valid_sort_fields)}."}), 400

    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction: '{direction}'. Must be 'asc' or 'desc'."}), 400

    # Default: unsorted
    sorted_posts = POSTS

    if sort:
        reverse = (direction == 'desc')
        sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=reverse)

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    endpoint for adding a new post
    :return: json with new post and 201 created
    """
    # here go's the endpoint for adding a post
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content"}), 400
    if len(data['title']) > 1000:
        return jsonify({"error": "Title too long"}), 400
    if len(data['content']) > 1000:
        return jsonify({"error": "Content too long"}), 400

    new_post = {
        'id': max([post['id'] for post in POSTS], default=0) + 1,
        'title': data['title'],
        'content': data['content'],
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201  # 201 = Created


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    endpoint for deleting a post
    :param id: id of post
    :return: json with deleted post with ok, 200
    """
    # Checks if id in POSTS id's
    found_post = next((post for post in POSTS if post['id'] == id), None)

    if not found_post:
        return jsonify({"error": "Post not found"}), 404
    else:
        POSTS.remove(found_post)
        return jsonify(found_post), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Endpoint for updating a post. Checks user input for emptiness
    or too loong inputs.
    :param id: id of post
    :return: JSON with updated post, 200
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400
    if 'title' not in data and 'content' not in data:
        return jsonify({"error": "Missing input, at least one of title or content must be provided."}), 400
    if 'title' in data and len(data['title']) > 100:
        return jsonify({"error": "Title too long"}), 400
    if 'content' in data and len(data['content']) > 500:
        return jsonify({"error": "Content too long"}), 400

    find_post = next((post for post in POSTS if post['id'] == id), None)

    if not find_post:
        return jsonify({"error": "Post not found"}), 404

    if 'title' in data:
        find_post['title'] = data['title']
    if 'content' in data:
        find_post['content'] = data['content']

    return jsonify(find_post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    endpoint for searching posts for title or content
    :return: JSON with the fitting posts, or all posts if nothing is found
    """
    title = request.args.get('title')
    content = request.args.get('content')

    # No filters case
    if not title and not content:
        return jsonify(POSTS), 200

    filtered = []
    for post in POSTS:
        title_match = title and title in post['title']
        content_match = content and content in post['content']

        if title_match or content_match:
            filtered.append(post)

    return jsonify(filtered), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
