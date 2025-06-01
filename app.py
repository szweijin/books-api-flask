from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# 自動讀取環境變數 DATABASE_URL（Render 會提供）
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 模型
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    language = db.Column(db.String)
    discount = db.Column(db.Float)
    price = db.Column(db.Float)
    link = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "language": self.language,
            "discount": self.discount,
            "price": self.price,
            "link": self.link
        }

@app.route("/")
def index():
    return "Welcome to the Book API! Visit /books to see the list."

# 路由：取得所有書籍
@app.route("/books")
def get_books():
    keyword = request.args.get("keyword", "")
    query = Book.query
    if keyword:
        keyword = f"%{keyword}%"
        query = query.filter(
            db.or_(Book.title.like(keyword), Book.author.like(keyword))
        )
    books = query.all()
    return jsonify([book.to_dict() for book in books])

# 路由：取得特定書籍
@app.route("/books/<int:book_id>")
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
