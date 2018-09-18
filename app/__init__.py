
from flask import Flask,jsonify,request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mm = Marshmallow(app)
#Table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(140))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#Object serialization and deserialization lib
class Schema(mm.Schema):
    class Meta:
        fields = ('id','title', 'body','date')
        ordered = True

pSchema = Schema()
postsSchema = Schema(many=True)

# API ROUTING
@app.route("/api/add", methods=["POST"])
def new_post():
    title = request.json['title']
    body = request.json['body']
    new_post = Post(title=title,body=body)
    print(new_post)
    print(new_post.title)
    print(new_post.body)
    print(new_post.date)
    db.session.add(new_post)
    db.session.commit()
    result = pSchema.dump(new_post)
    return jsonify(result.data)

@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    result = postsSchema.dump(posts)
    return jsonify(result.data)

@app.route("/api/post/<id>", methods=["GET"])
def get_post(id):
    post = Post.query.get(id)
    result = pSchema.dump(post)
    return jsonify(result)
