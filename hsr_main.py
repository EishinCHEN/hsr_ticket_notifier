import requests
import bs4
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from line_notifier import send_text_message

# 裝載連假售票資訊
@dataclass
class HolidayInfo:
  holiday_name: str
  holiday_perid: str
  saleing_date: date

holidays = []

# 取得高鐵公告連假售票資訊
response = requests.get("https://www.thsrc.com.tw/ArticleContent/60dbfb79-ac20-4280-8ffb-b09e7c94f043")
soup = bs4.BeautifulSoup(response.text, "html.parser")

# 取得表格區塊
news = soup.find("div", class_ = "news")
year = news.find("caption").text

# 需將bs4.element.ResultSet轉換為enumerate才可迭代
for index, item in enumerate(news.find_all("tr")):
  # 從第二筆開始擷取資料
  if index == 0:
    continue
  tds = item.find_all("td")
  holidays.append(HolidayInfo(tds[0].text, tds[1].text, datetime.strptime(tds[2].text.split(' ')[0], "%Y/%m/%d").date()))
  

# 取得今天和明天的日期
today = datetime.today().date()
tomorrow = today + timedelta(days = 1)
holidays.append(HolidayInfo("測試", "2025/01/23 (四) ~ 2025/02/03 (一)", tomorrow))

for holidaysItem in holidays:
  print(holidaysItem)
  if(holidaysItem.saleing_date == tomorrow):
    send_text_message(f"{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假高鐵車票將於{holidaysItem.saleing_date}開始販售")