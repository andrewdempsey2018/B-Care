import os

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# grab the enviornment variables
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# mongo db name is 'breastcancer'
# stories held in 'stories' collection
# information held in 'info' collection
storyData = mongo.db.stories
infoData = mongo.db.info

@app.route("/")
def index():
    return render_template("index.html", latestStory = storyData.find_one())

@app.route("/stories")
def stories():
    return render_template("stories.html", stories = storyData.find())

@app.route("/create_story")
def create_story():
    return render_template("create_story.html")

@app.route("/edit_story_page")
def edit_story_page():
    storyId=request.args.get("storyId", None)
    return render_template("edit_story_page.html", story=storyData.find_one({ '_id': ObjectId(storyId)}))

@app.route("/delete_story")
def delete_story():
    storyId=request.args.get("storyId", None)
    storyData.remove({ "_id": ObjectId(storyId) })
    return redirect(url_for("stories"))

@app.route("/publish_story", methods=["POST"])
def publish_story():
    storys=storyData
    storys.insert_one(request.form.to_dict())
    return redirect(url_for('stories'))

@app.route('/edit_story', methods=["POST"])
def edit_story():
    storyId=request.args.get('storyId', None)
    storys = storyData
    storys.update( {'_id': ObjectId(storyId)},
    {
        'title':request.form.get('title'),
        'text':request.form.get('text'),
    })
    return redirect(url_for('stories'))

# a page for viewing a single story on its own
# @app.route("/dedicated")
# def dedicated():
#    storyId = request.args.get('storyId', None)
#    return render_template("dedicated.html", story=storyData.find_one({ '_id': ObjectId(storyId) }))

# ------------------------------------------ #

# ------------------------------------------ #
@app.route("/speak")
def speak():
    return render_template("speak.html")
# ------------------------------------------ #

@app.route("/information")
def information():
    return render_template("information.html", allInfo = infoData.find())

@app.route("/edit_info_page")
def edit_info_page():
    infoId=request.args.get("infoId", None)
    return render_template("edit_info_page.html", info=infoData.find_one({ '_id': ObjectId(infoId)}))

@app.route('/edit_info', methods=["POST"])
def edit_info():
    infoId=request.args.get('infoId', None)
    infos = infoData
    infos.update( {'_id': ObjectId(infoId)},
    {
        'title':request.form.get('title'),
        'text':request.form.get('text'),
    })
    return redirect(url_for('information'))

@app.route("/new_info")
def new_info():
    return render_template("new_info.html")

@app.route("/publish_info", methods=["POST"])
def publish_info():
    infos=infoData
    infos.insert_one(request.form.to_dict())
    return redirect(url_for('information'))

@app.route("/delete_info")
def delete_info():
    infoId=request.args.get("infoId", None)
    infoData.remove({ "_id": ObjectId(infoId) })
    return redirect(url_for("information"))

# ------------------------------------------ #

@app.route("/login")
def login():
    return render_template("login.html")

# ------------------------------------------ #

# set to False (deploy) set to True (development)
if __name__ == '__main__':
    app.run(debug=True)