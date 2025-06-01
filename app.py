from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(100))
    language = db.Column(db.String(50))
    discount = db.Column(db.Float)
    price = db.Column(db.Float)
    link = db.Column(db.String(300))

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
    return "Welcome to the Book API! Visit /books or /dashboard."

@app.route("/books")
def get_books():
    keyword = request.args.get("keyword", "")
    query = Book.query
    if keyword:
        keyword = f"%{keyword}%"
        query = query.filter(or_(Book.title.like(keyword), Book.author.like(keyword)))
    books = query.all()
    return jsonify([book.to_dict() for book in books])

@app.route("/books/<int:book_id>")
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@app.route("/dashboard")
def dashboard():
    books = Book.query.all()
    return render_template("dashboard.html", books=books)

@app.route("/trends")
def trends():
    return render_template("trends.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
