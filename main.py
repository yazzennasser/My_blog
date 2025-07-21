from flask import Flask, render_template
from post import Post
import requests
import json

response = requests.get("https://api.npoint.io/32daa2c4dbd5e82bc4ed")

try:
    posts = response.json()
except json.JSONDecodeError:
    posts = []

if isinstance(posts, dict):
    posts = posts.get("posts", [])

if not isinstance(posts, list):
    posts = []

post_objects = []
for post in posts:
    if isinstance(post, dict):
        try:
            post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
            post_objects.append(post_obj)
        except KeyError:
            pass

app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next((p for p in post_objects if p.id == index), None)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
