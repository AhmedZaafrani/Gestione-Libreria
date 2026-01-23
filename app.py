from flask import Flask, jsonify, request
from faker import Faker
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

fake = Faker()
books = []

@app.route('/')
def index():
    return "Libreria API"

@app.route('/fake-books')
def gen_books():
    n = min(max(int(request.args.get('n', 5)), 1), 100)
    
    if request.args.get('reset'):
        books.clear()

    new_books = []
    for _ in range(n):
        book = {
            'id': fake.unique.uuid4(),
            'title': fake.sentence(nb_words=4).rstrip('.'),
            'author': fake.name(),
            'genre': fake.random_element(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Mystery', 'Romance', 'Horror']),
            'year_published': fake.year(),
            'isbn': fake.isbn13(),
        }
        new_books.append(book)
        books.append(book)

    return jsonify({'generated_count': n, 'generated': new_books, 'total_stored': len(books), 'data': books})

@app.route('/fake-users')
def fake_users():
    return gen_books()

@app.route('/data', methods=['GET', 'DELETE'])
def data():
    if request.method == 'DELETE':
        books.clear()
        return jsonify({'total_stored': 0, 'data': []})
    return jsonify({'total_stored': len(books), 'data': books})

@app.route('/book', methods=['POST'])
def add():
    body = request.get_json() or {}
    book = {
        'id': fake.unique.uuid4(),
        'title': body.get('title', fake.sentence(nb_words=4).rstrip('.')),
        'author': body.get('author', fake.name()),
        'genre': body.get('genre', fake.random_element(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Mystery'])),
        'year_published': body.get('year_published', fake.year()),
        'isbn': body.get('isbn', fake.isbn13()),
    }
    books.append(book)
    return jsonify(book), 201

@app.route('/book/<book_id>', methods=['DELETE'])
def delete(book_id):
    global books
    original = len(books)
    books = [b for b in books if b['id'] != book_id]
    if len(books) < original:
        return jsonify({'deleted': book_id, 'total_stored': len(books)})
    return jsonify({'error': 'not found'}), 404

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    limit = min(int(request.args.get('limit', 50)), 100)
    
    if not q:
        return jsonify({'count': 0, 'results': []})

    results = [b for b in books if q in b.get('author', '').lower()][:limit]
    return jsonify({'count': len(results), 'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
