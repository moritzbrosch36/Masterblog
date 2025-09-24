from flask import Flask, render_template, request, redirect, url_for
import json
import os

FILE_PATH = "blog_posts.json"

app = Flask(__name__)

if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


def load_posts():
    with open(FILE_PATH, "r", encoding="utf-8") as handle:
        posts = json.load(handle)
        # Falls Likes fehlen, ergänzen
        for post in posts:
            if "likes" not in post:
                post["likes"] = 0
        return posts


def save_posts(posts):
    with open(FILE_PATH, "w", encoding="utf-8") as handle:
        json.dump(posts, handle, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_posts()

        new_id = max([p["id"] for p in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"]
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            break
    save_posts(posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form["author"]
        post["title"] = request.form["title"]
        post["content"] = request.form["content"]

        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        post["likes"] += 1
        save_posts(posts)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)