from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from backend.models import GoogleAccount
from backend.models import Document
from backend.models import UserHandbook
from backend.models import Repetition

from .handbook import getUserHandbook

from mindojopolicy.settings import(
    MINDOJO_HANDBOOK_REVIEW_DAYS,
    MINDOJO_REPETITION_REVIEW_DAYS,
    HANDBOOK_REVIEW_DAYS_FIRST
)

def getUsers(admin_id):
    admin = User.objects.get(id=admin_id)
    if not admin.is_superuser:
        response = {
            "code": 400,
            "message": "You are not an admin."
        }
        return response
    users = User.objects.filter(is_active=True).values('id', 'first_name', 'last_name', 'email', 'date_joined')
    response = []
    for user in users:
        
        gaccount = GoogleAccount.objects.filter(user_id=user['id'])
        user['gavatar'] = ''
        if len(gaccount) > 0:
            user['gavatar'] = gaccount.last().gavatar
        #get status
        status = True
        dueDate = None
        overDue = False
        # handBookItems = list(UserHandbook.objects.filter(user=user['id'], finished=False).values('document', 'first', 'created_at').order_by('created_at').distinct())
        handBookItems = list(UserHandbook.objects.filter(user=user['id'], finished=False).values('document', 'first', 'document__updated_at').order_by('document__updated_at').distinct())
        
        if not len(handBookItems) == 0:
            status = False
            hbFirst = handBookItems[0]  #first handbook item
            if hbFirst['first']:  # first hand book after sign in
                dueDate = user['date_joined'] + datetime.timedelta(days = HANDBOOK_REVIEW_DAYS_FIRST)
            else:
                dueDate = hbFirst['document__updated_at'] + datetime.timedelta(days = MINDOJO_HANDBOOK_REVIEW_DAYS)
               
        repetitions = Repetition.objects.filter(user=user['id']).order_by('userrep_id')
        
        if not len(repetitions) == 0:
            
            repetition = repetitions.last()
            if repetition.finished == False:
                repDate = repetition.created_at + datetime.timedelta(days=MINDOJO_REPETITION_REVIEW_DAYS)
                if dueDate == None or dueDate > repDate:
                    dueDate = repDate
                status = False

        if not dueDate == None and timezone.now() > dueDate:
            overDue = True  

        user['status'] = status
        user['dueon'] = dueDate
        user['overDue'] = overDue
        response.append(user)
     
    return response

def getUserDocuments(admin_id, user_id):
    admin = User.objects.get(id=admin_id)
    if not admin.is_superuser:
        response = {
            "code": 400,
            "message": "You are not an admin"
        }
        return response

    response = getUserHandbook(user_id)

    return response
    