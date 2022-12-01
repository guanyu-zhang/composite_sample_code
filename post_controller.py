from flask import Flask, Response, request
from flask_cors import CORS
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
CORS(app)
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Post id={self.id} authorId={self.authorId} title={self.title} content={self.content}>"

    def toJson(self):
        return {
            "id": self.id,
            "authorId": self.authorId,
            "title": self.title,
            "content": self.content,
        }


@app.route("/posts/user/<int:userId>")
def getPostsByUserId(userId):
    res = db.session.query(Post).filter_by(authorId=userId).all()
    data = [r.toJson() for r in res] if res else []
    return Response(json.dumps({"data": data}))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
