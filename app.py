from flask import Flask, render_template
import json

FILE_PATH = "blog_posts.json"

app = Flask(__name__)


@app.route('/')
def index():
    with open(FILE_PATH, "r", encoding="utf-8") as handle:
        blog_posts = json.load(handle)
    return render_template("index.html", posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)