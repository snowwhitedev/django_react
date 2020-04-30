import datetime

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from backend.models import UserHandbook
from backend.models import Repetition, RepetitionItem
from backend.models import Question
from backend.models import Document
from backend.models import PolicyItem

from backend.actions.notification.notifications import repetitionNotify
from backend.actions.external.ping import completeCurRepetition

from mindojopolicy.settings import (
    MINDOJO_HIGH_ITEM_POSTPONE_MONTHS,
    MINDOJO_MEDIUM_ITEM_POSTPONE_MONTHS,
    REPETITION_LENGTH_LIMIT,
    POLICY_ITEM_IMPORTANCE_HIGH,
    POLICY_ITEM_IMPORTANCE_MEDIUM,
    POLICY_ITEM_IMPORTANCE_LOW,
    ANSWER_NOT_RECALL_AT_ALL,
    ANSWER_MORE_OR_LESS,
    ANSWER_PERFECTLY,
    MINDOJO_REPETITION_REVIEW_DAYS
)

def finishedRepetition(user):
    repetitions = Repetition.objects.filter(user=user)
    if len(repetitions) == 0:
        return True
        
    maxUserrep = repetitions.order_by('userrep_id').values('userrep_id', 'finished').last()
    return maxUserrep['finished']

def getUserRepetition(user_id):
    repetition = Repetition.objects.filter(user_id=user_id).order_by('userrep_id').last()
    userRepetition = RepetitionItem.objects.filter(repetition=repetition).values('id', 'itemNo', 'repetition', 'answer', 'policy', 'question_id').order_by('itemNo')
    repData = []
    for item in userRepetition:
        if not item['answer'] == -1:
            continue
        question = Question.objects.get(id=item['question_id'])
        item['question'] = question.question
        item['questionAns'] = question.answer
        repData.append(item)
    
    total = len(userRepetition)
    passed = total - len(repData)
    overdue = False
    dueon = ''
    
    if not repetition == None:
        dueon = repetition.created_at + datetime.timedelta(days=MINDOJO_REPETITION_REVIEW_DAYS)
        if dueon < timezone.now():
            overdue = True
    
    response = {"total": total, "passed":passed, "dueon":dueon, "overdue":overdue, "data": repData}
    return response

def answerUserRepetition(id, ans, user_id):
    repItem = RepetitionItem.objects.get(id=id)
    #check validate user
    rep = repItem.repetition_id
    repetition = Repetition.objects.get(id=rep)
    if not repetition.user_id == user_id:
        response = {"code": 400, "message":"Wrong API call."}
        return response
    
    if not repItem.answer == -1:
        response = {"code": 400, "message":"You have already answered this repetition item."}
        return response
    
    repItem.answer = ans
    repItem.answered_at = timezone.now()
    repItem.save()
    
    remainItems = RepetitionItem.objects.filter(repetition_id=rep, answer=-1)
    if len(remainItems) == 0:
        repetition.finished = True
        repetition.save()
        
    response = {"code": 200}
    completeCurRepetition(user_id)
    return response
