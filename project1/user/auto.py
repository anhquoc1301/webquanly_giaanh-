import datetime
from datetime import  datetime
from .nvr_api import downloadListPlates
def auto_download():
    x=datetime.now()
    if x.hour==0 and x.minute==1:
        downloadListPlates((datetime(year=x.year, month=x.month, day=x.day)))


