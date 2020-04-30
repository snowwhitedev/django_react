from django.contrib.auth.models import User

from backend.models import InitialComplete
from backend.models import UserHandbook
from backend.models import Repetition

# import requests
import requests
import os

from mindojopolicy.settings import (
    MINDOJO_EXTERNAL_URL_ENDPOINT,
    MINDOJO_EXTERNAL_EVENT_COMPLETE_FIRST_DOCUMENT_WORKFLOW_ID,
    MINDOJO_EXTERNAL_EVENT_COMPLETE_REPETITION_WORKFLOW_ID,
    MINDOJO_EXTERNAL_EVENT_COMPLETE_FIRST_DOCUMENT_STAGE_ID,
    MINDOJO_EXTERNAL_EVENT_COMPLETE_REPETITION_STAGE_ID
)

def completeInitialDoc(user_id):
    comp = InitialComplete.objects.filter(user_id=user_id)
    if len(comp) > 0:
        return False
    
    uhb = UserHandbook.objects.filter(user_id=user_id, finished=False)
    if len(uhb) == 0:
        externalUrl = MINDOJO_EXTERNAL_URL_ENDPOINT
        user = User.objects.get(id=user_id)
        json = {
            'email': user.email,
            'workflow_id': MINDOJO_EXTERNAL_EVENT_COMPLETE_FIRST_DOCUMENT_WORKFLOW_ID,
            'stage_id':MINDOJO_EXTERNAL_EVENT_COMPLETE_FIRST_DOCUMENT_STAGE_ID
        }
        requests.post(externalUrl, json=json)

        iniComp = InitialComplete()
        iniComp.user = user
        iniComp.status = True
        iniComp.save()
    return True

def completeCurRepetition(user_id):
    curRep = Repetition.objects.filter(user_id=user_id).values('finished').order_by('userrep_id').last()
    if curRep['finished'] == True:
        externalUrl = MINDOJO_EXTERNAL_URL_ENDPOINT
        user = User.objects.get(id=user_id)
        json = {
            'email': user.email,
            'workflow_id': MINDOJO_EXTERNAL_EVENT_COMPLETE_REPETITION_WORKFLOW_ID,
            'stage_id': MINDOJO_EXTERNAL_EVENT_COMPLETE_REPETITION_STAGE_ID
        }
        requests.post(externalUrl, json=json)
    return