import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# PostgreSQL 資料庫連線設定
db_user = "books_db_bzdg_user"
db_password = "H3TcEfiraF7aTurlb5ERm3Qn2KgCugDd"
db_host = "dpg-d0u0q3k9c44c73a36r00-a"
db_port = "5432"
db_name = "books_db_bzdg"

# 建立 SQLAlchemy 的 Engine
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# 讀取 CSV 檔案
df = pd.read_csv("books_python.csv")

# 欄位名稱需與資料表欄位一致
df.columns = ["title", "author", "language", "discount", "price", "link"]

# 匯入資料到 PostgreSQL 的 books 資料表
df.to_sql("book", engine, if_exists="append", index=False)

print("✅ 書籍資料已成功匯入 PostgreSQL！")
