from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug import debug
import gevent
import os

live_userlist = ""

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
socketio = SocketIO(app)

# grab the enviornment variables
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# mongo db name is 'breastcancer'
# stories held in 'stories' collection
# information held in 'info' collection
storyData = mongo.db.stories
infoData = mongo.db.info
newsData = mongo.db.news
userData = mongo.db.users
chatUsers = mongo.db.chat_users

if os.environ.get("DEBUG") == 'True':
    app.debug = True
else:
    app.debug = False


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        existing_user = userData.find_one(
            {"username": request.form.get("username")})
        if(existing_user):
            user = request.form.get("username")
            if(existing_user["password"] == request.form.get("password")):
                session["user"] = user
                return render_template("index.html", latestStory=storyData.find_one(), user=user, news=newsData.find())
            else:
                flash("Incorrect password")
                session["user"] = "guest"
                return render_template("login.html", user=session["user"])
        else:
            flash("No user account with this name exists")
            session["user"] = "guest"
            return render_template("login.html", user=session["user"])
    else:
        if(session.get('user')):
            return render_template("index.html", latestStory=storyData.find_one(), user=session["user"], news=newsData.find())
        else:
            session["user"] = "guest"
            return render_template("index.html", latestStory=storyData.find_one(), user=session["user"], news=newsData.find())


@app.route("/stories")
def stories():
    return render_template("stories.html", stories=storyData.find(), user=session["user"])


@app.route("/create_story")
def create_story():
    return render_template("create_story.html", user=session["user"])


@app.route("/edit_story_page")
def edit_story_page():
    storyId = request.args.get("storyId", None)
    return render_template("edit_story_page.html", story=storyData.find_one({'_id': ObjectId(storyId)}))


@app.route("/delete_story")
def delete_story():
    storyId = request.args.get("storyId", None)
    storyData.remove({"_id": ObjectId(storyId)})
    return redirect(url_for("stories"))


@app.route("/publish_story", methods=["POST"])
def publish_story():
    storys = storyData
    storys.insert_one(request.form.to_dict())
    return redirect(url_for('stories'))


@app.route('/edit_story', methods=["POST"])
def edit_story():
    storyId = request.args.get('storyId', None)
    storys = storyData
    storys.update({'_id': ObjectId(storyId)},
                  {
        'title': request.form.get('title'),
        'text': request.form.get('text'),
    })
    return redirect(url_for('stories'))

# a page for viewing a single story on its own
# @app.route("/dedicated")
# def dedicated():
#    storyId = request.args.get('storyId', None)
#    return render_template("dedicated.html", story=storyData.find_one({ '_id': ObjectId(storyId) }))

# ------------------------------------------ #

# a page for viewing a single story on its own


@app.route("/news_full")
def news_full():
    newsId = request.args.get('newsId', None)
    return render_template("news_full.html", article=newsData.find_one({'_id': ObjectId(newsId)}))

# ------------------------------------------ #


@app.route("/news")
def news():
    return render_template("news.html", user=session["user"], news=newsData.find())

# ------------------------------------------ #


@app.route("/speak")
def speak():
    return render_template("speak.html", user=session["user"])
# ------------------------------------------ #


@app.route("/delete_admin")
def delete_admin():
    userId = request.args.get("userId", None)
    userData.remove({"_id": ObjectId(userId)})
    return redirect(url_for("admin"))
# ------------------------------------------ #


@app.route("/information")
def information():
    return render_template("information.html", allInfo=infoData.find(), user=session["user"])


@app.route("/edit_info_page")
def edit_info_page():
    infoId = request.args.get("infoId", None)
    return render_template("edit_info_page.html", info=infoData.find_one({'_id': ObjectId(infoId)}))


@app.route('/edit_info', methods=["POST"])
def edit_info():
    infoId = request.args.get('infoId', None)
    infos = infoData
    infos.update({'_id': ObjectId(infoId)},
                 {
        'title': request.form.get('title'),
        'text': request.form.get('text'),
    })
    return redirect(url_for('information'))


@app.route("/new_info")
def new_info():
    return render_template("new_info.html")


@app.route("/publish_info", methods=["POST"])
def publish_info():
    infos = infoData
    infos.insert_one(request.form.to_dict())
    return redirect(url_for('information'))


@app.route("/delete_info")
def delete_info():
    infoId = request.args.get("infoId", None)
    infoData.remove({"_id": ObjectId(infoId)})
    return redirect(url_for("information"))

# ------------------------------------------ #


@app.route("/login_page")
def login_page():
    return render_template("login.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user")
    session['user'] = "guest"
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    return render_template("admin.html", users=userData.find())


@app.route("/register_page")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    users = userData
    users.insert_one(request.form.to_dict())
    flash(request.form.to_dict())
    return redirect(url_for('register_page'))

# ------------------------------------------ #

# Creat custom error pages
# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal server error


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# ------------------------------------------ #


@app.route("/chat")
def chat():
    return render_template("chat.html", user=session["user"])

# server receives messages through the message 'route'
# sends the message to ALL clients connected....


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    socketio.emit('updateui', data)

# ------------------------------------------ #

@socketio.on('connect')
def test_connect():

    # user connects to chat room, add name to database
    chatUsers.insert_one({"name": session["user"]})

    # get all usernames stored in the database
    clients=chatUsers.find()

    # parse all usernames into a list so that we may send it to the clients local chat.js
    # so that it may be used to updaate their user interface showing a complete list of connected clients
    client_names=[]
    for client in clients:
        client_names.append(client['name'])

    # send the list of client names to socket io for transmission to all clients using the 'update_userlist' socket io route
    socketio.emit('update_userlist', client_names)
    print('Client connected')

# remove remove this particular client name from the database when they leave the chatroom
@socketio.on('disconnect')
def test_disconnect():
    chatUsers.delete_one({"name": session["user"]})
    socketio.emit('update_userlist', chatUsers.distinct('name'))
    print('Client disconnected')

# ------------------------------------------ #

# if os tells app to run in debug mode, socket io
# will be turned off. For production, socket IO
# will be on

if __name__ == '__main__':
    if app.debug:
        app.run()
    else:
        socketio.run(app)

# ------------------------------------------ #
