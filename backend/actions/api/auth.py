import re
from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from backend.models import EmailPattern
# from django.contrib.auth.models import Group
from backend.models import GoogleAccount
from backend.models import Repetition

from backend.actions.api.repetition import finishedRepetition

admin.site.unregister(Token)

from backend.actions.notification.notifications import repetitionNotify

def signin(userData):
    email = userData['email']
    user = User.objects.filter(email=email)
    
    if len(user) == 0:
        if not signup(userData):
            response = {
                'code': 400,
                'message': 'Sorry, Sign Up failed',
            }
            return response
    
    curUser = User.objects.get(email=email)
    if not curUser.is_active:
        response = {
            'code': 400,
            'message': 'Sorry, you are not acitvated now',
        }
        return response
    
    if curUser.is_superuser or curUser.is_staff:
        token = Token.objects.get_or_create(user=curUser)
        finishedRep = finishedRepetition(curUser)
        response = {
            'code': 200,
            'token': token[0].key,
            'user_id': curUser.id,
            'isAdmin': curUser.is_superuser,
            'finishedRepetition': finishedRep
        }
        return response
    
    response = {
        'code': 400,
        'message': 'Sorry, you are not our member yet.'
    }

    return response

def signup(userData):
    patterns = EmailPattern.objects.all()
    for pattern in patterns:
        regExp = ".*" + pattern.pattern + "$"
        if re.match(regExp, userData['email']):
            try:
                user = User()
                user.email = userData['email']
                # user.username = userData['username']
                user.username = userData['first_name'] + userData['last_name']
                user.first_name = userData['first_name']
                user.last_name = userData['last_name']
                user.is_active = True
                user.is_staff  = True
                user.save()
                gacc = GoogleAccount()
                gacc.user_id = user.id
                gacc.gavatar = userData['gavatar']
                gacc.save()
                return True
            except:
                return False
    
    return False
