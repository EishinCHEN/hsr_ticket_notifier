from datetime import date, datetime, timedelta
from hsr_spider import fetch_holiday_info
from line_notifier import send_text_message

def check_and_notify_holidays(holidays: list):
  """檢查明天是否有高鐵售票，若有則發送通知，若無則告知服務正常運行"""
  today = datetime.today().date()
  tomorrow = today + timedelta(days = 1)
  
  found_sale = False
  for holidaysItem in holidays:
    if(holidaysItem.saleing_date == tomorrow):
      message = f"{holidaysItem.holiday_perid}{holidaysItem.holiday_name}連假高鐵車票將於{holidaysItem.saleing_date}開始販售"
      send_text_message(message) # 發送售票通知
      found_sale = True
      break

  if not found_sale:
    message = "目前明天沒有高鐵連假售票資訊，服務能運行正常中~"
    send_text_message(message)  # 發送正常運行通知

def main():
  holidays = fetch_holiday_info()
  check_and_notify_holidays(holidays)

if __name__ == "__main__":
    main()