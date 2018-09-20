
from flask import Flask,jsonify,request,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mm = Marshmallow(app)

def create_app(config_class=Config):
    # ...
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app
#Table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(140))
    date = db.Column(db.Date, index=True, default=datetime.utcnow().date())

class Schema(mm.Schema):
    class Meta:
        fields = ('id','title', 'body','date')
        ordered = True

pSchema = Schema()
postsSchema = Schema(many=True)
 
# API ROUTING
@app.route("/api/add", methods=["POST"])
def new_post():
    title = request.form['title']
    body = request.form['body']
    new_post = Post(title=title,body=body)
    db.session.add(new_post)
    db.session.commit()
    result = pSchema.dump(new_post)
    return render_template("base.html")
"""
Aslında ilk başta yazdığımda json verisi gönderirim diye düşünüyordum, sonrasında tekrar uğraşmamak için form şeklinde değiştirdim.

@app.route("/api/add", methods=["POST"])
def new_post():
    title = request.json['title']
    body = request.json['body']
    new_post = Post(title=title,body=body)
    db.session.add(new_post)
    db.session.commit()
    result = pSchema.dump(new_post)
    return render_template("base.html")

"""

@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    result = postsSchema.dump(posts)
    return jsonify(result.data)

@app.route("/api/post/<id>", methods=["GET"])
def get_post(id):
    post = Post.query.get(id)
    result = pSchema.dump(post)
    return jsonify(result.data)


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")