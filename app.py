
from flask import Flask, jsonify, request
from faker import Faker
from flask_cors import CORS

app = Flask(__name__)
faker = Faker()

# Allow cross-origin requests (from React dev server or other origins)
CORS(app)

# In-memory store for generated profiles
data = []

@app.route('/')
def index():
    return 


@app.route('/fake-users')
def fake_users():
    n = 5

    # support reset flag to clear stored data
    reset_flag = request.args.get('reset', '').lower() in ('1', 'true', 'yes')
    if reset_flag:
        data.clear()

    generated = []
    for _ in range(n):
        profile = {
            'name': faker.name(),
            'email': faker.email(),
            'address': faker.address().replace('\n', ', '),
            'phone_number': faker.phone_number(),
            'job': faker.job(),
            'company': faker.company(),
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
