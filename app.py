
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


@app.route('/fake-users')
def fake_users():
    # read query param 'n' for how many to generate (default 5)
    try:
        n = int(request.args.get('n', 5))
    except (TypeError, ValueError):
        n = 5

    # bound n
    n = max(1, min(n, 100))

    # support reset flag to clear stored data
    reset_flag = request.args.get('reset', '').lower() in ('1', 'true', 'yes')
    if reset_flag:
        data.clear()

    generated = []
    for _ in range(n):
        profile = {
            'id': faker.unique.uuid4(),
            'name': faker.name(),
            'email': faker.email(),
            'address': faker.address().replace('\n', ', '),
            'phone_number': faker.phone_number(),
            'job': faker.job(),
            'company': faker.company(),
        }
        # optional ssn
        try:
            profile['ssn'] = faker.ssn()
        except Exception:
            profile['ssn'] = None

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
    results = [u for u in data if q_lower in u.get('name', '').lower()]
    return jsonify({'count': len(results[:limit]), 'results': results[:limit]})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
