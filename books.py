from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# 啟動瀏覽器
driver = webdriver.Chrome()

# 搜尋關鍵字
keyword = "python"
url = f"https://search.books.com.tw/search/query/key/{keyword}/cat/all"

driver.get(url)
time.sleep(3)  # 等待網頁載入

# 建立一個清單來儲存所有書籍資料
book_data = []
page_max = 10
page_count = 1  # 初始為第 1 頁

while True:
    print(f"正在擷取第 {page_count} 頁...")
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    books = soup.select("div.table-td")

    for book in books:
        title_tag = book.select_one("h4 a")
        if not title_tag:
            continue

        info_tags = book.select("div.type p")
        price_tags = book.select("ul.price b")


        title = title_tag.text.strip() if title_tag else "N/A"
        link = "https:" + title_tag['href'] if title_tag else "N/A"
        author = info_tags[1].text.strip() if len(info_tags) > 1 else "N/A"
        language = info_tags[0].text.strip() if len(info_tags) > 0 else "N/A"

        if len(price_tags) >= 2:
            discount = price_tags[0].text.strip()
            price = price_tags[1].text.strip()
        elif len(price_tags) == 1:
            discount = None
            price = price_tags[0].text.strip()
        else:
            discount = None
            price = None

        book_data.append({
            "書名": title,
            "作者": author,
            "語言": language,
            "折扣": discount,
            "價格": price,
            "連結": link
        })

    # 判斷是否超過最多頁數
    if page_count >= page_max:
        print("已達最大頁數限制")
        break

    try:
        next_btn = driver.find_element("css selector", "a.next")
        next_btn.click()
        page_count += 1
        time.sleep(3)
    except:
        print("已無下一頁")
        break

driver.quit()

# 將結果轉為 DataFrame 並儲存為 CSV
df = pd.DataFrame(book_data)
df.to_csv("books_python.csv", index=False, encoding="utf-8-sig")
print("資料已儲存至 books_python.csv")
