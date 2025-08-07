from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)
url_mapping = {}

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# 🆕 Add this route
@app.route('/')
def home():
    return "URL Shortener is running!"

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({'error': 'No URL provided'}), 400
    short = generate_short_url()
    url_mapping[short] = original_url
    # Fix: generate short URL using actual domain
    short_url = request.host_url + short
    return jsonify({'short_url': short_url})


@app.route('/<short>')
def redirect_url(short):
    url = url_mapping.get(short)
    if url:
        return jsonify({'redirect_to': url})
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
