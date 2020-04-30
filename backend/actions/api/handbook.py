from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.utils import timezone
import datetime

# from dateutil

from backend.models import UserHandbook
from backend.models import Document
from backend.models import PolicyItem
from backend.models import DocumentStructure

from backend.actions.external.ping import completeInitialDoc

from mindojopolicy.settings import (
    HANDBOOK_REVIEW_DAYS_FIRST,
    MINDOJO_HANDBOOK_REVIEW_DAYS
)

def getUserHandbook(user_id):
    docAll = UserHandbook.objects.filter(user_id=user_id).values( 'document__id', 'document__title', 'document__description', 'finished', 'first', 'created_at', 'document', 'user__date_joined').order_by('document__title','created_at').distinct()
    docIds = UserHandbook.objects.filter(user_id=user_id).values( 'document__id').distinct()
    docjoins = list()
    
    for docId in docIds:
        docHbTemp = list(docAll.filter(document_id=docId['document__id']).order_by('created_at'))
        if len(docHbTemp) == 0:
            continue

        docjoins.append(docHbTemp[0])

    documentSet = list()
    for doc in docjoins:
        hbs = docAll.filter(document_id=doc['document__id']).values('finished', 'first').distinct()
        
        if any( hb['finished'] == False for hb in hbs):
            doc['finished'] = False
        else:
            doc['finished'] = True

        if any( hb['first'] == True for hb in hbs):
            doc['first'] = True
        else:
            doc['first'] = False

        dueDays = MINDOJO_HANDBOOK_REVIEW_DAYS
        if doc['first']:
            dueDays = HANDBOOK_REVIEW_DAYS_FIRST
            dueDate = doc['user__date_joined'] + datetime.timedelta(days=dueDays)
        else:
            dueDate = doc['created_at'] + datetime.timedelta(days=dueDays)

        overDue = False
        if timezone.now() > dueDate:
            overDue = True
        
        doc['dueon'] = dueDate
        doc['overdue'] = overDue
        doc['document__description'] = doc['document__description']
        documentSet.append(doc)
    
    response = documentSet
    return response

def getPolicyItems(user_id, document_id):

    selDocument = DocumentStructure.objects.filter(document_id=document_id).order_by('id')

    data = list()
    for sd in selDocument:
        poGroup = list()
        for policy in sd.policyitems.all().values('id', 'itemText', 'importance'):
            handBookInstance = UserHandbook.objects.get(user_id=user_id, policy_id=policy['id'])
            
            policy['finished'] = handBookInstance.finished
            poGroup.append(policy)
        
        data.append({'description':sd.description, 'policyGroup': poGroup})

    response = data
    return response

def checkPolicyItem(user_id, policy_id):
    handBook = UserHandbook.objects.filter(user_id=user_id).get(policy_id=policy_id)
    handBook.finished = True
    handBook.first = False
    # try:
    handBook.save()
    response = {"message": "checked"}
    completeInitialDoc(user_id)
    return response
    
def getDocuments(user_id):
    documentSet = {"document": "document"}
    response = documentSet
    return response