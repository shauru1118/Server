from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

VIEWS_DIR = os.path.join(os.path.dirname(__file__), "views")

@app.route("/")
@app.route("/home")
def home():
    return send_from_directory(VIEWS_DIR, "index.html")

@app.route("/<path:filename>")
def serve_page(filename):
    filepath = os.path.join(VIEWS_DIR, filename)
    if os.path.exists(filepath):
        return send_from_directory(VIEWS_DIR, filename)
    else:
        return send_from_directory(VIEWS_DIR, "404.html"), 404

if __name__ == "__main__":
    print(VIEWS_DIR)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
