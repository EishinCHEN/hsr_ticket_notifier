A Python-based LINE Bot that automatically sends notifications when Taiwan High-Speed Rail (HSR) and Taiwan Railway (TRA) releases pre-sale tickets during consecutive holidays. 
It scrapes data from the official HSR and TRA website and uses LINE Notify to send timely alerts to users.

一款自動化 LINE Bot，針對台灣高鐵於連假期間的預售票開放日，主動發送通知提醒使用者購票。</br>
透過網頁爬蟲擷取高鐵官網資訊，結合 LINE Notify 自動化傳送通知。</br>
LINE ID：@011iduiw</br>

Tech Stack:
- Python (Requests, BeautifulSoup)
- LINE Notify integration
- Scheduled tasks via cron
  
<div style="display: flex; justify-content: center; gap: 10px;">
  <img src="https://github.com/EishinCHEN/hsr_ticket_notifier/blob/64a8d52da5ca6a60c7a2a4a4e75032468c403765/images/line_bot.jpg" style="height: 300px; object-fit: contain;">
  <img src="https://github.com/EishinCHEN/hsr_ticket_notifier/blob/5ae11f759423fdca57130dd76d961122e95ec09e/images/messageInfo.jpg" style="height: 300px; object-fit: contain;">
</div>
