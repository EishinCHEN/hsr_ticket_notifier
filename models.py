from dataclasses import dataclass
from datetime import date

# 裝載連假售票資訊
@dataclass
class HolidayInfo:
    company_name: str
    holiday_name: str
    holiday_perid: str
    saleing_date: date