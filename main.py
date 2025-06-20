import json
import random
from datetime import date, datetime, timedelta
from hsr_spider import fetch_hsr_holiday_info
from tra_spider import fetch_tra_holiday_info
from line_notifier import send_text_message

def check_and_notify_holidays(holidays: list):
    """檢查明天是否有售票，若有則發送通知，若無則告知服務正常運行"""
    # 讀取 JSON 訊息模板
    with open("messages.json", "r", encoding="utf-8") as file:
        messages_data = json.load(file)

    today = datetime.today().date()
    tomorrow = today + timedelta(days = 1)
    closest_holiday_name = None
    closest_holiday_date = None
    started_presale_holiday_name = None
    found_sale = False
    
    for holidaysItem in holidays:
        # 檢查最近的節日與售票日期
        if holidaysItem.saleing_date and holidaysItem.saleing_date > today:
            if closest_holiday_date is None or holidaysItem.saleing_date < closest_holiday_date:
                closest_holiday_date = holidaysItem.saleing_date
                closest_holiday_name = holidaysItem.holiday_name
        
        # 檢查最近一個已經開始販售車票的節日
        if holidaysItem.saleing_date and holidaysItem.saleing_date == today:
            started_presale_holiday_name = holidaysItem.holiday_name
            match holidaysItem.company_name:
                case "hsr":
                    message = random.choice(messages_data["presale_started_beginning"]) + started_presale_holiday_name +random.choice(messages_data["presale_started_hsr_area"])
                case "tra":
                    message = random.choice(messages_data["presale_started_beginning"]) + started_presale_holiday_name +random.choice(messages_data["presale_started_tra_area"])
            
            send_text_message(message)
            found_sale = True

        # 檢查是否為明天售票
        if holidaysItem.saleing_date and holidaysItem.saleing_date == tomorrow:
            match holidaysItem.company_name:
                case "hsr":
                    random_presale_day_beginning_message = random.choice(messages_data["presale_day_beginning"])
                    random_presale_day_info_area_message = random.choice(messages_data["hsr_holiday_info_area"])
                    random_presale_day_ending_message = random.choice(messages_data["presale_day_ending"])
                    message = random_presale_day_beginning_message + holidaysItem.holiday_name + random_presale_day_info_area_message + holidaysItem.holiday_perid + random_presale_day_ending_message
                case "tra":
                    random_presale_day_beginning_message = random.choice(messages_data["presale_day_beginning"])
                    random_presale_day_info_area_message = random.choice(messages_data["tra_holiday_info_area"])
                    random_presale_day_ending_message = random.choice(messages_data["presale_day_ending"])
                    message = random_presale_day_beginning_message + holidaysItem.holiday_name + random_presale_day_info_area_message + holidaysItem.holiday_perid + random_presale_day_ending_message
      
            send_text_message(message) # 發送售票通知
            found_sale = True

    # 待售票資訊迭待完成再寄送正常運行通知
    if not found_sale:
        # 組合訊息內容
        random_normal_day_beginning_message = random.choice(messages_data["normal_day_beginning"])
        random_normal_day_ending_message = random.choice(messages_data["normal_day_ending"])
        message = random_normal_day_beginning_message + closest_holiday_name + random_normal_day_ending_message
        send_text_message(message)  # 發送正常運行通知

def main():
    holidays = fetch_hsr_holiday_info() + fetch_tra_holiday_info()
    check_and_notify_holidays(holidays)

if __name__ == "__main__":
    main()