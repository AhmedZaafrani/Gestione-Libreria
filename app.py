
from flask import Flask, jsonify, request
from faker import Faker
from flask_cors import CORS

app = Flask(__name__)
faker = Faker()

# enable CORS for React frontend
CORS(app)
# In-memory store for generated books
data = []

@app.route('/')
def index():
    return "Welcome to the Fake Users API"


@app.route('/fake-books')
def fake_books():
    """Generate fake books and store them in `data`.

    Query params:
      - n: number to generate (default 5, max 100)
      - reset: if '1' or 'true', clear stored data before generating
    """
    try:
        n = int(request.args.get('n', 5))
    except (TypeError, ValueError):
        n = 5

    n = max(1, min(n, 100))

    reset_flag = request.args.get('reset', '').lower() in ('1', 'true', 'yes')
    if reset_flag:
        data.clear()

    generated = []
    for _ in range(n):
        # Use generic providers to avoid missing provider errors
        book = {
            'id': faker.unique.uuid4(),
            'title': faker.sentence(nb_words=4).rstrip('.'),
            'author': faker.name(),
            'genre': faker.random_element(elements=('Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Horror')),
            'year_published': faker.year(),
            'isbn': faker.isbn13(),
        }
        generated.append(book)

    data.extend(generated)

    return jsonify({
        'generated_count': n,
        'generated': generated,
        'total_stored': len(data),
        'data': data,
    })


@app.route('/fake-users')
def fake_users_alias():
    """Alias for /fake-books to keep compatibility with frontend calls to /fake-users."""
    return fake_books()


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
