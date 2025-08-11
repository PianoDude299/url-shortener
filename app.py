from flask import Flask, request, redirect, render_template, url_for
import string
import random

app = Flask(__name__)

# In-memory storage for shortened URLs
url_mapping = {}

# Function to generate random short codes
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        original_url = request.form["url"].strip()
        if original_url:
            short_code = generate_short_code()
            while short_code in url_mapping:  # Avoid duplicates
                short_code = generate_short_code()
            url_mapping[short_code] = original_url
            short_url = request.host_url + short_code
    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
