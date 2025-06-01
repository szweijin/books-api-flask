import schedule
import time
import import_books_to_postgres

def job():
    print("開始自動匯入資料...")
    import_books_to_postgres.import_books()

schedule.every(60).minutes.do(job)

if __name__ == "__main__":
    print("Scheduler 啟動")
    while True:
        schedule.run_pending()
        time.sleep(1)
