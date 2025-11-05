import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ========== 热榜来源 ==========
SOURCES = {
    "知乎": "https://www.zhihu.com/billboard",
    "微博": "https://s.weibo.com/top/summary",
    "36氪": "https://36kr.com/hot-list",
    "虎嗅": "https://www.huxiu.com/channel/106.html",
    "懂车帝": "https://www.dongchedi.com/news"
}

# 关键词筛选
KEYWORDS = ["汽车", "理想", "比亚迪", "特斯拉", "奔驰", "宝马", "大众", "蔚来", "极氪", "智界", "问界"]

# ========== 爬取函数 ==========
def fetch_hot_topics():
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for name, url in SOURCES.items():
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text()
            found = False
            for kw in KEYWORDS:
                if kw in text:
                    results.append(f"{name} 有关于『{kw}』的热议话题")
                    found = True
                    break
            if not found:
                results.append(f"{name} 暂无汽车相关热榜")
        except Exception as e:
            results.append(f"{name} 抓取失败: {e}")
    return results

# ========== 保存文件函数 ==========
def save_file(content):
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"daily_hot_topics_{date_str}.html"
    html_content = f"""
    <html>
    <head><meta charset="utf-8"><title>汽车热议榜-{date_str}</title></head>
    <body>
        <h2>汽车热议榜 - {datetime.now().strftime('%Y-%m-%d')}</h2>
        <ul>
    """
    for item in content:
        html_content += f"<li>{item}</li>\n"
    html_content += """
        </ul>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 文件已生成: {filename}")

# ========== 主程序 ==========
if __name__ == "__main__":
    topics = fetch_hot_topics()
    save_file(topics)
