from django.contrib.auth.models import User
from django.utils import timezone
import time
import datetime
from dateutil.relativedelta import relativedelta

from backend.models import CronLog
# from backend.actions.api.repetition import createRepetitionItems
from backend.actions.notification.notifications import repetitionNotify

from django.contrib.auth.models import Group
from django.utils import timezone
from backend.models import UserHandbook
from backend.models import Repetition, RepetitionItem
from backend.models import Question
from backend.models import Document
from backend.models import PolicyItem

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
    REPETITION_UPDATE_PERIOD
)

def refreshRepetitions():
    # print("[cron]-refresh repetition")
    # cronlog = CronLog()
    # cronlog.description = "refresh repetition"
    # activeUsers = User.objects.filter(is_active=True)
    # cronlog.userNumber = len(activeUsers)
    # cronlog.save()

    for user in activeUsers:
        curRep = Repetition.objects.filter(user=user).order_by('userrep_id').values('created_at', 'finished').last()
        if not curRep == None:
            lastCreated = curRep['created_at']
            # if lastCreated + datetime.timedelta(days=REPETITION_UPDATE_PERIOD) < timezone.now():
            print("last created", REPETITION_UPDATE_PERIOD)
            print("[created]",lastCreated + relativedelta(months=REPETITION_UPDATE_PERIOD))
            if lastCreated + relativedelta(months=REPETITION_UPDATE_PERIOD) < timezone.now():
                print("[refresh repetitions")
            # if lastCreated + datetime.timedelta(days=0) < timezone.now():
                createRepetitionItems(user.id)
                time.sleep(2)
        else:
            createRepetitionItems(user.id)
            time.sleep(2)

def createRepetition(user_id):
    repetition = Repetition()
    repetition.user_id = user_id
    lastRep = Repetition.objects.filter(user_id=user_id).order_by('userrep_id').values('userrep_id', 'finished').last()
    if lastRep == None:
        repetition.userrep_id = 1
    else:
        maxRepId = lastRep['userrep_id']
        repetition.userrep_id = maxRepId + 1
    repetition.save()

    return repetition

#repetition item table
def createRepetitionItems(user_id):
    userPolicies = UserHandbook.objects.filter(user_id=user_id, finished=True).values('policy')
    preRepetitions = list(Repetition.objects.filter(user_id=user_id).order_by('userrep_id'))

    policyCandidates = list()
    for up in userPolicies:
        policyQuestions = Question.objects.filter(policy_id=up['policy'])
       
        if len(policyQuestions) == 0:
            continue
        
        #check high or medium level items which is not seen for long time 
        policy = PolicyItem.objects.get(id=up['policy'])
        importance = policy.importance
               
        if not importance == POLICY_ITEM_IMPORTANCE_LOW:
            relRepsByUser = Repetition.objects.filter(user_id=user_id)
            relRepItems = RepetitionItem.objects.filter(repetition__in=relRepsByUser, policy_id=up['policy'])

            relReps = list(RepetitionItem.objects.filter(policy_id=up['policy'], repetition__user_id=user_id).values( 'repetition__id', 'repetition__created_at', 'repetition__userrep_id').order_by('repetition__created_at').distinct())
            
            if len(relReps) > 0: # not the first time to create repetition
                lastShow = relReps[-1]['repetition__created_at']
                
                if importance == POLICY_ITEM_IMPORTANCE_HIGH:
                    limitDate = lastShow + datetime.timedelta(MINDOJO_HIGH_ITEM_POSTPONE_MONTHS * 365 / 12)
                elif importance == POLICY_ITEM_IMPORTANCE_MEDIUM:
                    limitDate = lastShow + datetime.timedelta(MINDOJO_MEDIUM_ITEM_POSTPONE_MONTHS * 365 / 12)
                
                if limitDate < timezone.now():
                    policyCandidates.append({'policy': up, 'score': POLICY_ITEM_IMPORTANCE_HIGH * ANSWER_NOT_RECALL_AT_ALL + importance})
                    continue
            else:
                if len(preRepetitions) == 0:
                    pass
                else:
                    firstRep = Repetition.objects.get(user_id=user_id, userrep_id=1)
                    firstShow = firstRep.created_at
                    
                    if importance == POLICY_ITEM_IMPORTANCE_HIGH:
                        limitDate = firstShow + datetime.timedelta(MINDOJO_HIGH_ITEM_POSTPONE_MONTHS * 365 / 12)
                    elif importance == POLICY_ITEM_IMPORTANCE_MEDIUM:
                        limitDate = firstShow + datetime.timedelta(MINDOJO_MEDIUM_ITEM_POSTPONE_MONTHS * 365 / 12)
                    
                    if limitDate < timezone.now():
                        policyCandidates.append({'policy': up, 'score': POLICY_ITEM_IMPORTANCE_HIGH * ANSWER_NOT_RECALL_AT_ALL + importance})
                        continue
        
        ans1 = ANSWER_NOT_RECALL_AT_ALL # for the answer of the last repetition
        ans2 = ANSWER_NOT_RECALL_AT_ALL # for the answer of the before last repetition
        
        if len(preRepetitions) > 0: # if this policy item(-up-) has been appeared at least one times
            try:
                answer1 = RepetitionItem.objects.get(policy_id=up['policy'], repetition=preRepetitions[-1])
                ans1 = answer1.answer
            except:
                pass
        if len(preRepetitions) > 1: # if this policy item(-up-) has been appeared at least two times
            try:
                answer2 = RepetitionItem.objects.get(policy_id=up['policy'], repetition=preRepetitions[-2])
                ans2 = answer1.answer
            except:
                pass
        
        ans = (ans1 + ans2) / 2 # average answer
        policy = PolicyItem.objects.get(id=up['policy'])
        score = ans * policy.importance
        policyCandidates.append({'policy': policy, 'score': score})
    
    policyCandidates = sorted(policyCandidates, key=lambda k: k['score'], reverse=True)
    policies = policyCandidates[:REPETITION_LENGTH_LIMIT]

    if len(policies) == 0:
        return
        
    itemNo = 1
    repetition = createRepetition(user_id)
    
    for policy in policies:
        repetitionItem = RepetitionItem()
        repetitionItem.policy = policy['policy']
        repetitionItem.itemNo = itemNo
        repetitionItem.repetition = repetition

        #select question
        policyQuestions = Question.objects.filter(policy_id=policy['policy'].id)
        
        pqCands = []
        neverShowedFound = False #if find policy question never shown
        for pq in policyQuestions:
            pqReps = RepetitionItem.objects.filter(question=pq).values('repetition') #repetitions involved policy questions 

            if len(pqReps) == 0: # never used question
                repetitionItem.question = pq
                neverShowedFound = True
                break

            pqRepIds = list(map(lambda ri: ri["repetition"], pqReps))
            pqRepetitions = Repetition.objects.filter(id__in=pqRepIds).filter(user_id=user_id).order_by('created_at')  # get the repetition assigned this question to this user
            
            if len(pqRepetitions) <= 1: # never used question
                repetitionItem.question = pq
                neverShowedFound = True
                break

            lastShowed = pqRepetitions.last()
            pqCands.append({'question': pq, 'showed_at': lastShowed.created_at})

        if not neverShowedFound:
            pqCands = sorted(pqCands, key=lambda k: k['showed_at'])
            repetitionItem.question = pqCands[0]['question']
        
        repetitionItem.save()
        itemNo += 1
    
    repetitionNotify(user_id)
    return True