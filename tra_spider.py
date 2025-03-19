import requests
import bs4
from models import HolidayInfo 
from datetime import datetime

def fetch_tra_holiday_info() -> list[HolidayInfo]:
    # 取得台鐵公告連假售票資訊
    response = requests.get("https://www.railway.gov.tw/tra-tip-web/tip/tip00C/tipC21/view?subCode=8ae4cac28d0e8e3d018d131085d908fe")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # 取得表格區塊
    holidays = []
    news = soup.find('div', class_ = "adm-article").find("table")
    for index, item in enumerate(news.find_all("tr")):
        tds = item.find_all("td") 
        match index:
            case 0 | 2:
                # 跳過標題列、春節連假第二列
                continue
            case 1:
                holiday_name = tds[0].text
                saleing_date = convert_to_datetime(tds[1].text)
                holidays.append(HolidayInfo("tra", holiday_name, tds[3].text, saleing_date)) 
            case _:
                holiday_name = tds[0].find("p").text
                saleing_date = convert_to_datetime(tds[1].text)
                holidays.append(HolidayInfo("tra", holiday_name, tds[3].text, saleing_date))
    return holidays

def convert_to_datetime(saleing_date_str):
    # 範例資料 "12/03 (三) 零時"
    saleing_date_str = saleing_date_str.strip() # 移除前後空白
    saleing_date_str = saleing_date_str.split('(')[0] # 移除 ( 後面字樣

    # 民國年轉換成西元年
    parts = saleing_date_str.split('/')
    if len(parts) == 3:
        year = int(parts[0])+1911 # 民國轉西元
        month = int(parts[1])
        day = int(parts[2])
        return datetime(year, month, day).date()
    if len(parts) == 2:
        year = datetime.today().date().year # 取得今天的年份
        month = int(parts[0])
        day = int(parts[1])
        return datetime(year, month, day).date()
    return None