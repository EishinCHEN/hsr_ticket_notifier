from datetime import date, datetime, timedelta
from hsr_spider import fetch_hsr_holiday_info
from tra_spider import fetch_tra_holiday_info
from line_notifier import send_text_message

def check_and_notify_holidays(holidays: list):
    """檢查明天是否有售票，若有則發送通知，若無則告知服務正常運行"""
    today = datetime.today().date()
    tomorrow = today + timedelta(days = 1)
  
    found_sale = False
    for holidaysItem in holidays:
        if(holidaysItem.saleing_date == tomorrow):
            match holidaysItem.company_name:
                case "hsr":
                    message = f"{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假高鐵車票將於{holidaysItem.saleing_date}開始販售"
                case "tra":
                    message = f"{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假台鐵車票將於{holidaysItem.saleing_date}開始販售"
      
            send_text_message(message) # 發送售票通知
            found_sale = True
            break

    # 待售票資訊迭待完成再寄送正常運行通知
    if not found_sale:
        message = "欸欸！都幾點了！ 回家沒？\n 啊還有我看過了啦！ \n明天不會賣連假的票 \n 今天可以去睡覺了啦！"
        send_text_message(message)  # 發送正常運行通知

def main():
    holidays = fetch_hsr_holiday_info() + fetch_tra_holiday_info()
    check_and_notify_holidays(holidays)

if __name__ == "__main__":
    main()