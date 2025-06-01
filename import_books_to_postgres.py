import pandas as pd
from sqlalchemy import create_engine

def import_books():
    db_user = "books_db_bzdg_user"
    db_password = "H3TcEfiraF7aTurlb5ERm3Qn2KgCugDd"
    db_host = "dpg-d0u0q3k9c44c73a36r00-a.singapore-postgres.render.com"
    db_port = "5432"
    db_name = "books_db_bzdg"

    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    df = pd.read_csv("books_python.csv")
    df.columns = ["title", "author", "language", "discount", "price", "link"]

    df.to_sql("book", engine, if_exists="append", index=False)

    print("✅ 書籍資料已成功匯入 PostgreSQL！")

if __name__ == "__main__":
    import_books()
