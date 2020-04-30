from django.utils import timezone
import datetime

def formatDate(dt):
    return dt.strftime("%b %d %Y %H:%M:%S")