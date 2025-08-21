from datetime import datetime
import pytz

IDAYS = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]

def now_id(tz="Asia/Jakarta"):
    z = pytz.timezone(tz)
    return datetime.now(z)

def fmt_full_ts(dt):
    hari = IDAYS[dt.weekday()]
    return f"{hari}, {dt.day} {dt.strftime('%B %Y %H:%M:%S')}"

def fmt_uptime(seconds:int):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
