# init_db.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 資料模型
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    language = db.Column(db.String)
    discount = db.Column(db.Float)
    price = db.Column(db.Float)
    link = db.Column(db.String)

# 將折扣欄位轉換的函數
def convert_discount(val):
    if pd.isnull(val):
        return None
    try:
        # 例如 "79折" 轉換成浮點數 7.9 再乘以 0.1 變為 0.79
        return float(str(val).replace("折", "")) * 0.1
    except Exception as e:
        return None

# 建立資料表並匯入 CSV
def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        df = pd.read_csv("books_python.csv")
        # 清洗價格欄位：移除非數字字元並轉換為 float
        df["價格"] = df["價格"].replace(r"[^\d.]", "", regex=True).astype(float)
        # 處理折扣欄位：利用自定義函數
        df["折扣"] = df["折扣"].apply(convert_discount)

        for _, row in df.iterrows():
            book = Book(
                title=row["書名"],
                author=row["作者"],
                language=row["語言"],
                discount=row["折扣"],
                price=row["價格"],
                link=row["連結"]
            )
            db.session.add(book)
        db.session.commit()
        print("📚 書籍資料已成功匯入資料庫 books.db")

if __name__ == "__main__":
    init_database()
