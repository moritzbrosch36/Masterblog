from flask import Flask, render_template, request, redirect, url_for
import json

FILE_PATH = "blog_posts.json"

app = Flask(__name__)

def load_posts():
    with open(FILE_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)

def save_posts(posts):
    with open(FILE_PATH, "w", encoding="utf-8") as handle:
        json.dump(posts, handle, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()

        new_post = {
            "id": len(posts) + 1,
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"]
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            break
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)