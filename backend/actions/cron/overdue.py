from django.contrib.auth.models import User
from django.utils import timezone
import time
import datetime

from backend.models import CronLog
from backend.models import UserHandbook
from backend.models import Repetition
from backend.models import RepetitionItem

from backend.actions.notification.notifications import overDueHandBookNotification, overDueRepetitionNotification

from mindojopolicy.settings import(
    MINDOJO_HANDBOOK_REVIEW_DAYS,
    MINDOJO_REPETITION_REVIEW_DAYS
)

def overDueHandbook():
    cronlog = CronLog()
    cronlog.description = "over due handbook"
    cronlog.save()
    # unFinishedHBs = UserHandbook.objects.filter(finished=False).values('document_id', 'user_id', 'document__updated_at').distinct()
    # unFinishedHBs = UserHandbook.objects.filter(finished=False).values('document_id', 'user_id', 'document__updated_at').distinct()
    # sentUsers = []
    # for hb in unFinishedHBs:
    #     if hb['document__updated_at'] + datetime.timedelta(days=MINDOJO_HANDBOOK_REVIEW_DAYS) < timezone.now() and not unFinishedHBs['user_id'] in set(sentUsers):
            
    #         sentUsers.append(unFinishedHBs['user_id'])
    overDueHandBookNotification()

def overDueRepetition():
    # cronlog = CronLog()
    # cronlog.description = "over due repetition"
    # cronlog.save()
    print("overdue repetition")
    # overDueRepetitionNotification()
        
