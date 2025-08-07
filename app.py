from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)
url_mapping = {}

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({'error': 'No URL provided'}), 400
    short = generate_short_url()
    url_mapping[short] = original_url
    return jsonify({'short_url': f"http://localhost:5000/{short}"})

@app.route('/<short>')
def redirect_url(short):
    url = url_mapping.get(short)
    if url:
        return jsonify({'redirect_to': url})
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
