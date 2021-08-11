"""
Example post representation in the database:

{
  "title": "Based Post",
  "content": "allo",
  "tags": [
    "based",
    "entrepreneur"
  ],
  "upvotes": 0,
  "downvotes": 0,
  "reports": 0,
  "id": 123245123124,
  "parent": 85718975819651, // null if the post is a thread
  "image": null,
  "date": ISODate("2021-08-03T15:14:27.817Z"),
}
"""
try:
    from flask import Flask, render_template, redirect, send_from_directory
    from flask import request as req
    from flask.helpers import url_for
    from pymongo import MongoClient
    from datetime import datetime
    from werkzeug.utils import secure_filename
    from pathlib import Path
    from Pac.pac import parents_and_children
except ImportError:
    print("Please 'pip install' the specified module from the PyPi Server!")


app = Flask(__name__)


# Attempt to create 4fun's upload folder. Exit if permission denied
app.config["UPLOAD_FOLDER"] = "/opt/4fun/uploads/"
upload_folder = Path(app.config["UPLOAD_FOLDER"])
if not upload_folder.exists():
    try:
        upload_folder.mkdir(exist_ok=True)
    except PermissionError:
        print(f"Please create {upload_folder}")
        exit(1)


mongoclient = MongoClient()
db = mongoclient["4fun"]
posts = db["posts"]
counters = db["counters"]

if counters.estimated_document_count() == 0:
    counters.insert_one({"coll": "posts", "last_index": 0})


def id_for_new_post():
    """
    Get a new unused ID for a post. IDs are auto incremented
    """
    last_indx_doc = counters.find_one_and_update(
        {"coll": "posts"}, {"$inc": {"last_index": 1}}, new=True
    )
    return last_indx_doc["last_index"]


@app.route("/")
def index():
    all_posts = list(posts.find({}))
    posts_by_id = {p["id"]: p for p in all_posts}
    threads = parents_and_children(all_posts)
    try:
        return render_template("index.html", threads=threads, posts_by_id=posts_by_id)
    except:
        print("Cannot render the index.html file, please check your templates folder for the index.html file!")


@app.route("/new-post", methods=["POST"])
def new_post(**overrides):
    base_post = {
        "title": req.form.get("title", None),
        "content": req.form["content"],
        "tags": [],
        "upvotes": 0,
        "downvotes": 0,
        "reports": 0,
        "parent": None,
        "id": id_for_new_post(),
        "image": None,
        "date": datetime.now(),
    }

    if req.form.get("tags"):
        base_post["tags"] = req.form["tags"].split(",")

    uploaded_img = req.files.get("image", None)
    if uploaded_img:
        filename = secure_filename(uploaded_img.filename)
        uploaded_img.save(upload_folder / filename)
        base_post["image"] = filename

    posts.insert_one({**base_post, **overrides})
    return redirect("/")


@app.route("/reply/<int:post_id>", methods=["GET", "POST"])
def reply(post_id):
    # reply input page, not submitting yet
    if req.method == "GET":
        post = posts.find_one({"id": post_id})
        title = post["title"] or str(post["id"])
        return render_template("reply.html", post=post, title=title)
    # actual POST submission endpoint
    else:
        return new_post(content=req.form["content"], parent=int(req.form["parent"]))

@app.route("/img/<img_path>")
def img(img_path):
    try:
        return send_from_directory(str(upload_folder.absolute()), img_path)
    except:
        print("cannot download the image!")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
# run with https
# mkdir ssl && openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365 -subj "/C=US/ST=New York/L=New York/O=General Org/OU=Ou/CN=example.com"
# app.run(host='0.0.0.0', port='443', ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
