
from flask import Flask, jsonify, request
from faker import Faker
from flask_cors import CORS

app = Flask(__name__)
faker = Faker()

# In-memory store for generated profiles
data = []

@app.route('/')
def index():
    return "Welcome to the Fake Users API"


@app.route('/fake-Books')
def fake_users():
    n = 20  # Default number of profiles to generate

    generated = []
    for _ in range(n):
        profile = {
            'id': faker.unique.uuid4(),
            'title': faker.book.title(),
            'author': faker.book.author(),
            'genre': faker.random_element(elements=('Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Horror')),   
            'year_published': faker.year(),
            'isbn': faker.isbn13(),
        }
        generated.append(profile)

    data.extend(generated)

    return jsonify({
        'generated_count': n,
        'generated': generated,
        'total_stored': len(data),
        'data': data,
    })


@app.route('/data')
def show_data():
    """Return the list of currently stored generated profiles."""
    return jsonify({'total_stored': len(data), 'data': data})


@app.route('/search')
def search_users():
    """Search stored users by name (case-insensitive substring).

    Query params:
      - q: query string to search in the user name
      - limit: optional max number of results (default 50)
    """
    q = request.args.get('q', '')
    try:
        limit = int(request.args.get('limit', 50))
    except (TypeError, ValueError):
        limit = 50

    if not q:
        return jsonify({'count': 0, 'results': []})

    q_lower = q.strip().lower()
    results = [u for u in data if q_lower in u.get('author', '').lower()]
    return jsonify({'count': len(results[:limit]), 'results': results[:limit]})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
