from flask import Flask, Response, request
from flask_cors import CORS
import json, requests
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
CORS(app)
db = SQLAlchemy(app)
db.init_app(app)

POST_BASE_URL = "http://localhost:5001"  # modify this url accordingly


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    pwdHash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username} pwdHash={self.pwdHash}>"

    def toJson(self):
        return {
            "id": self.id,
            "username": self.username,
            "pwdHash": self.pwdHash,
        }


@app.route("/user/<int:userId>")
def getUserById(userId):
    user = db.session.query(User).filter_by(id=userId).first()
    res = user.toJson() if user else {}
    return Response(json.dumps(res))


@app.route("/user/<int:userId>/posts")  # composite service controller
def getPostsByUserId(userId):
    user = requests.get(f"{request.scheme}://{request.host}/user/{userId}").json()
    posts = requests.get(f"{POST_BASE_URL}/posts/user/{userId}").json()
    user.update(posts)
    return Response(json.dumps(user))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
