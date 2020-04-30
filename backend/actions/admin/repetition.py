from django.db import transaction
from django.db.utils import *

from django.contrib.auth.models import User
from backend.models import UserHandbook
from backend.models import Repetition
from backend.models import RepetitionItem
from backend.models import Question
from backend.models import PolicyItem

def deleteRepItemByDoc(pids):
    if len(pids.strip()) == 0:
        return 
    policyIds = pids.split(',')
    repItems = RepetitionItem.objects.filter(policy_id__in=policyIds)
    if len(repItems) > 0:
        repItems.delete()

def deleteRepItemByQuestion(qid):
    curRepItem = RepetitionItem.objects.filter(question_id=qid).order_by('repetition_id').last()
    if not curRepItem == None:
        curRepItem.delete()
