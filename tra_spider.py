import requests
import bs4
from models import HolidayInfo 

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
                holidays.append(HolidayInfo("tra", holiday_name, tds[3].text, tds[1].text)) 
                print(HolidayInfo(holiday_name, tds[3].text, tds[1].text))
            case _:
                holiday_name = tds[0].find("p").text
                holidays.append(HolidayInfo("tra", holiday_name, tds[3].text, tds[1].text))
                print(HolidayInfo(holiday_name, tds[3].text, tds[1].text))
    return holidays