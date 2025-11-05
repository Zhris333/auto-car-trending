import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# ========== 邮箱设置 ==========
SMTP_SERVER = "smtp.yeah.net"  # 你的邮箱SMTP服务器
SMTP_PORT = 465
EMAIL_ADDRESS = "chris_zhangjixin@yeah.net"  # 你的邮箱
EMAIL_PASSWORD = "你的授权码"  # ⚠️ 稍后用GitHub Secrets替代

# ========== 热榜来源 ==========
SOURCES = {
    "知乎": "https://www.zhihu.com/billboard",
    "微博": "https://s.weibo.com/top/summary",
    "36氪": "https://36kr.com/hot-list",
    "虎嗅": "https://www.huxiu.com/channel/106.html",
    "懂车帝": "https://www.dongchedi.com/news"
}

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
            for kw in KEYWORDS:
                if kw in text:
                    results.append(f"{name} 有关于『{kw}』的热议话题")
                    break
        except Exception as e:
            results.append(f"{name} 抓取失败: {e}")
    return results

# ========== 邮件函数 ==========
def send_email(content):
    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header("汽车热榜机器人", "utf-8")
    message["To"] = Header("Zhris", "utf-8")
    message["Subject"] = Header(f"今日汽车热议榜 - {datetime.now().strftime('%Y-%m-%d')}", "utf-8")

    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
        smtp.quit()
        print("✅ 邮件已发送成功！")
    except Exception as e:
        print("❌ 邮件发送失败:", e)

# ========== 主程序 ==========
if __name__ == "__main__":
    topics = fetch_hot_topics()
    content = "\n".join(topics) if topics else "今日暂无汽车相关热榜内容。"
    send_email(content)
