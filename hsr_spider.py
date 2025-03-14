import requests
import bs4
from dataclasses import dataclass
from datetime import date, datetime

# 裝載連假售票資訊
@dataclass
class HolidayInfo:
  holiday_name: str
  holiday_perid: str
  saleing_date: date

def fetch_holiday_info() -> list[HolidayInfo]:
  # 取得高鐵公告連假售票資訊
  response = requests.get("https://www.thsrc.com.tw/ArticleContent/60dbfb79-ac20-4280-8ffb-b09e7c94f043")
  soup = bs4.BeautifulSoup(response.text, "html.parser")

  # 取得表格區塊
  holidays = []
  news = soup.find("div", class_ = "news")

  # 需將bs4.element.ResultSet轉換為enumerate才可迭代
  for index, item in enumerate(news.find_all("tr")):
    # 跳過標題列 從第二筆開始擷取資料
    if index == 0:
      continue
    tds = item.find_all("td")
    saleing_date = datetime.strptime(tds[2].text.split(' ')[0], "%Y/%m/%d").date()
    holidays.append(HolidayInfo(tds[0].text, tds[1].text, saleing_date))

  return holidays