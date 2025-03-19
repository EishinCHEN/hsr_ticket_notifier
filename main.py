import json
import random
from datetime import date, datetime, timedelta
from hsr_spider import fetch_hsr_holiday_info
from tra_spider import fetch_tra_holiday_info
from line_notifier import send_text_message

def check_and_notify_holidays(holidays: list):
    """檢查明天是否有售票，若有則發送通知，若無則告知服務正常運行"""
    today = datetime.today().date()
    tomorrow = today + timedelta(days = 1)
  
    closest_holiday_name = None
    closest_holiday_date = None
    found_sale = False
    for holidaysItem in holidays:
        # 檢查最近的節日與售票日期
        if holidaysItem.saleing_date and holidaysItem.saleing_date >= today:
            if closest_holiday_date is None or holidaysItem.saleing_date < closest_holiday_date:
                closest_holiday_date = holidaysItem.saleing_date
                closest_holiday_name = holidaysItem.holiday_name
        
        # 檢查是否為明天售票
        if(holidaysItem.saleing_date == tomorrow):
            match holidaysItem.company_name:
                case "hsr":
                    message = f"小精靈重磅登場✨✨\n{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假高鐵車票將於{holidaysItem.saleing_date}開始販售"
                case "tra":
                    message = f"小精靈重磅登場✨✨\n{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假台鐵車票將於{holidaysItem.saleing_date}開始販售"
      
            send_text_message(message) # 發送售票通知
            found_sale = True
            break

    # 待售票資訊迭待完成再寄送正常運行通知
    if not found_sale:
        # 讀取 JSON 訊息模板
        with open("messages.json", "r", encoding="utf-8") as file:
            messages_data = json.load(file)
        
        # 組合訊息內容
        random_beginning_message = random.choice(messages_data["beginning"])
        random_ending_message = random.choice(messages_data["ending"])
        message = random_beginning_message+"\n明天沒有賣"+closest_holiday_name+"的票~"+random_ending_message
        send_text_message(message)  # 發送正常運行通知

def main():
    holidays = fetch_hsr_holiday_info() + fetch_tra_holiday_info()
    check_and_notify_holidays(holidays)

if __name__ == "__main__":
    main()