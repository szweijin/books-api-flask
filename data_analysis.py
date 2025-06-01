import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 設定中文字型（macOS）
matplotlib.rcParams['font.family'] = 'Heiti TC'
matplotlib.rcParams['axes.unicode_minus'] = False

# 讀取 CSV
df = pd.read_csv("books_python.csv")

# 顯示前幾筆資料
print(df.head())

# 將價格欄位轉為數字
df["價格"] = df["價格"].replace(r"[^\d.]", "", regex=True).astype(float)

# 處理折扣欄位
df["折扣"] = df["折扣"].astype(str).str.replace("折", "", regex=False)
df["折扣"] = pd.to_numeric(df["折扣"], errors="coerce")
df["折扣"] = df["折扣"].apply(lambda x: x * 0.1 if pd.notnull(x) else x)

# 移除價格為空值的資料
df = df.dropna(subset=["價格"])

plt.figure(figsize=(10, 5))
sns.histplot(df["價格"], bins=30, kde=True, color="skyblue")
plt.title("書籍價格分佈圖")
plt.xlabel("價格 (元)")
plt.ylabel("書籍數量")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x="折扣", y="價格", alpha=0.7)
plt.title("折扣 vs 價格")
plt.xlabel("折扣（0~1）")
plt.ylabel("價格")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
lang_counts = df["語言"].value_counts()
sns.barplot(x=lang_counts.index, y=lang_counts.values, hue=lang_counts.index, palette="Set2", legend=False)
plt.title("書籍語言統計")
plt.xlabel("語言類別")
plt.ylabel("書籍數量")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
