from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from backend.models import UserHandbook
from backend.models import Repetition
from backend.models import RepetitionItem

from django.template.loader import get_template
from backend.actions.common import formatDate
from backend.models import OverdueHandbook

from mindojopolicy.settings import (
    EMAIL_HOST,
    MINDOJO_EMAIL_SENDER,
    MINDOJO_REPETITION_REVIEW_DAYS,
    HANDBOOK_REVIEW_DAYS_FIRST,
    MINDOJO_HANDBOOK_REVIEW_DAYS,
    SERVER_URL,
    MINDOJO_ADMIN_EMAIL
)

def repetitionNotify(user_id):
    # print("notification repetition refreshed")
    subject = "Time to review some policy items"
    user = User.objects.filter(is_active=True, id=user_id).values('first_name', 'email').last()
    
    plainText = get_template('repetition_notification_template.html')
    
    dueDate = formatDate(timezone.now() + datetime.timedelta(MINDOJO_REPETITION_REVIEW_DAYS))
    d = { 'first_name': user['first_name'], "due_date": dueDate, 'link':  SERVER_URL + "/repetition"}
    message = plainText.render(d)
    # print(message)
    try:
        msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user['email']])
        msg.content_subtype = "html"
        msg.send()
    except:
        pass

def policyitemNotification(document):
    # print("notification policyitem changed", document.title)
    docTitle = document.title
    subject = "Title: Some policies were added/changed in " + docTitle + ", please review them."
    users = UserHandbook.objects.filter(user__is_active=True, document=document).values('user__first_name', 'user__email').distinct()

    plainText = get_template('policyitem_notification_template.html')
    
    for user in users:
        dueDate = formatDate(timezone.now() + datetime.timedelta(MINDOJO_HANDBOOK_REVIEW_DAYS))
        d = { 'first_name': user['user__first_name'], "title": docTitle, "due_date": dueDate, 'link':  SERVER_URL + "/policy"}
        message = plainText.render(d)
        # print("[notification]", user['user__email'])
        try:
            msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user['user__email']])
            msg.content_subtype = "html"
            msg.send()
        except:
            pass

def overDueHandBookNotification():
    # print("notification overdue handbook notification")
    subject = "You have overdue handbook pages and/or policy items to review"
    users = User.objects.filter(is_active=True).values('first_name', 'email', 'id')
    
    plainText = get_template('overdue_notification_template.html')
    
    for user in users:
        d = { 'link':  SERVER_URL + "/policy"}
        message = plainText.render(d)
        
        handbooks = UserHandbook.objects.filter(user_id=user['id'], finished=False).values('created_at', 'first')
        limitDate = timezone.now() - datetime.timedelta(days=MINDOJO_HANDBOOK_REVIEW_DAYS)
        
        if any( hb['first'] == True for  hb in handbooks):
            limitDate = timezone.now() - datetime.timedelta(days=HANDBOOK_REVIEW_DAYS_FIRST)
        
        if any( hb['created_at'] < limitDate for hb in handbooks):
            wkday = timezone.now().weekday()
            if wkday < 5:
                try:
                    #for debugging
                    print("[notification overdue handbook]", user['email'], limitDate)
                    pastOverdue = OverdueHandbook.objects.filter(user_id=user['id'])
                    if len(pastOverdue) == 0:
                        msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user['email']])
                        overdueHB = OverdueHandbook()
                        overdueHB.user_id = user['id']
                        overdueHB.overdue = 1
                        overdueHB.save()
                    else:
                        msg = EmailMessage( subject=subject, body=message, from_email=MINDOJO_EMAIL_SENDER, to=[user['email']], cc=[MINDOJO_ADMIN_EMAIL])
                    msg.content_subtype = "html"
                    msg.send()
                    print("[notification overdue handbook] - message was sent")
                except:
                    pass

#needless module
def overDueRepetitionNotification():
    # print("notification overdue repetition notification")
    subject = "You have overdue repetition to review"
    users = User.objects.filter(is_active=True).values('first_name', 'email', 'id')
    
    plainText = get_template('overdue_notification_template.html')

    for user in users:
        d = { 'link':  SERVER_URL + "/repetition"}
        message = plainText.render(d)
        limitDate = timezone.now() - datetime.timedelta(days=MINDOJO_REPETITION_REVIEW_DAYS)
        
        handbooks = UserHandbook.objects.filter(user_id=user['id'],finished=False).values('document__created_at')
    
        if any( hb['document__created_at'] < limitDate for hb in handbooks):
            wkday = timezone.now().weekday()
            if wkday < 5:
                try:
                    #for debugging
                    print("notification overdue repetition", user['email'], len(handbooks), MINDOJO_REPETITION_REVIEW_DAYS)
                    msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user['email']])
                    msg.content_subtype = "html"
                    msg.send()
                    print("[notification overdue repetition] - message was sent")
                except:
                    pass

# this notification would be sent when document group is saved 
def newDocNotification(users):
    # print("notification new document notification")
    subject = "You have new handbook pages for review"

    plainText = get_template('newdoc_notification_template.html')
    
    for user in users:
        
        d = { 'first_name':user.first_name, 'link':  SERVER_URL + "/policy"}
        message = plainText.render(d)
        # print("[notification] new user", user.email, message)
        try:
            msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user.email])
            msg.content_subtype = "html"
            msg.send()
        except:
            pass   

def newDocNotificationByUserGroup(userId):
    user = User.objects.get(id=userId)
    # print("notification new document notification by user-group")
    subject = "You have new handbook pages for review"
    plainText = get_template('newdoc_notification_template.html')
    d = { 'first_name':user.first_name, 'link':  SERVER_URL + "/policy"}
    message = plainText.render(d)
    # print("[notification document by user group] ", user.email, message)
    try:
        msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, [user.email])
        msg.content_subtype = "html"
        msg.send()
    except:
        pass