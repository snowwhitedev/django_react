from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.utils import *

from backend.models import UserHandbook
from backend.models import Document
from backend.models import PolicyItem
from backend.models import DocumentStructure

from backend.actions.notification.notifications import newDocNotification, newDocNotificationByUserGroup

CUSTOM_TAG_START = '@POLICYITEM'
CUSTOM_TAG_END = '@ENDPOLICYITEM'
ERROR = False
JOINSTRING = ","

#when saving document...
def saveUserHandbook(documentId, groups, policyItems, updatedPolicyIds):
    #convert update ids from string to int
    updatedPolicyIds = [int(idx) for idx in updatedPolicyIds]
    #previous users assigned to this document
    document = Document.objects.get(id=documentId)
    prevHBS = UserHandbook.objects.filter(document__id=documentId).values('user_id', 'policy_id').distinct()
    prevUserIds = list(pu['user_id'] for pu in prevHBS)
    
    prevUsers = User.objects.filter(id__in=prevUserIds)

    users = User.objects.filter(groups__in=groups).distinct()
    deletedUsers =  list(set(prevUsers) - set(users))
    newUsers = list(set(users) - set(prevUsers)) #for email notification
    #delete user handbook record of deleted users for this document from table
    UserHandbook.objects.filter(user__in=deletedUsers, document_id=documentId).delete()

    #update document remove records from table for deleted policy items
    prevPolIds = list(pu['policy_id'] for pu in prevHBS)
    if len(policyItems.strip()) == 0:
        policyIds = []
    else:
        polIdsTemp = policyItems.split(JOINSTRING)
        policyIds = [ int(idx) for idx in polIdsTemp ] 
    
    deletedPolIds = list(set(prevPolIds) - set(policyIds))
    UserHandbook.objects.filter(policy_id__in=deletedPolIds).delete()

    for user in users:
        for pId in policyIds:
            if len(policyItems.strip()) == 0:
                hbs = UserHandbook.objects.filter(user=user, document_id=documentId)
            else:
                hbs = UserHandbook.objects.filter(user=user, document_id=documentId, policy_id=pId)
            
            if len(hbs) == 0:
                userHandbook =  UserHandbook()
                userHandbook.user = user
                userHandbook.document_id = documentId
                if not len(policyItems.strip()) == 0:
                    userHandbook.policy_id = pId
            else:
                userHandbook = hbs.last()
                if pId in updatedPolicyIds: #for updated policy items
                    userHandbook.finished = False
            try:
                with transaction.atomic():
                    userHandbook.save()
            except IntegrityError:
                pass
    #email notification
    newDocNotification(newUsers)
    return 1

#when saving document save document structure too
def saveDocumentStructure(document):
    docBody = document.body
    docBody_cpy = docBody
    policyGroups = []
    curDescription = ''
    curPolIds = []

    while(1):
        tagStartPos = docBody_cpy.find(CUSTOM_TAG_START)
        if tagStartPos is -1:
            #todo exceptional case when have no any policy items
            policyGroups.append({'description': curDescription, 'policyItems': curPolIds})
            break
        between = docBody_cpy[:tagStartPos]
        if between.strip():
            if not len(curPolIds) == 0:
                policyGroups.append({'description': curDescription, 'policyItems': curPolIds})
            curDescription = between.strip()
            curPolIds = []
        
        docBody_cpy = docBody_cpy[tagStartPos + len(CUSTOM_TAG_START):]
        #find id like @POLICYITEM[132]
        if docBody_cpy[0] != '[':
            return ERROR

        idTagEnd = docBody_cpy.find(']')
        if idTagEnd is -1:
            return ERROR
        
        policyId = docBody_cpy[1: idTagEnd]
        if not policyId.isnumeric():
            return ERROR
        policyId = int(policyId)

        tagEndPos = docBody_cpy.find(CUSTOM_TAG_END)
        if tagEndPos is -1:
            return ERROR #error
        
        curPolIds.append(policyId)
        docBody_cpy = docBody_cpy[tagEndPos + len(CUSTOM_TAG_END):]
    
    if docBody_cpy.strip():
        policyGroups.append({'description':docBody_cpy.strip(), 'policyItems':[]})
    
    idx = 0
    for pg in policyGroups:
        docStructure = DocumentStructure.objects.filter(descriptionId=idx, document=document).last()
        if not docStructure:
            docStructure =  DocumentStructure()
        
        docStructure.descriptionId = idx
        docStructure.description = pg['description']
        docStructure.document = document
        docStructure.save()

        poItems = PolicyItem.objects.filter(id__in=pg['policyItems'])
        for po in poItems:
            docStructure.policyitems.add(po)
        idx += 1

    #delete records removed
    preItems = DocumentStructure.objects.filter(document=document).values('descriptionId')
    preIds = list(item['descriptionId'] for item in preItems)
    deletedIds = list(set(preIds) - set(list(range(idx))))
    DocumentStructure.objects.filter(document=document, descriptionId__in=deletedIds).delete()

# def deleteDocumentStructureByDoc(docId):
#     pass
#     # DocumentStructure.objects.filter(document_id=docId).delete()

def deleteHandbookByDoc(docId):
    relDocs = UserHandbook.objects.filter(document_id=docId)
    relDocs.delete()
    
#when user saving, --- depens on user --- groups
def saveHandbookByUser(user_id, groups):
    preDocuments = UserHandbook.objects.filter(user_id=user_id).values('document').distinct()
    first = False
    if len(preDocuments) == 0:
        first = True
    preDocIds = list(doc['document'] for doc in preDocuments)
    newDocuments = Document.objects.filter(groups__in=groups).values('id').distinct()
    newDocIds = list(doc['id'] for doc in newDocuments)
    
    #delete userhandbook record from table
    deletedDocIds = list(set(preDocIds) - set(newDocIds))
    UserHandbook.objects.filter(document_id__in=deletedDocIds).delete()

    for docId in newDocIds:
        policyItems = Document.objects.get(id=docId)
        policyIds = policyItems.policyItems.split(JOINSTRING)

        for pId in policyIds:
            userHandbook = UserHandbook()
            userHandbook.user_id = user_id
            userHandbook.document_id = docId
            userHandbook.policy_id = pId
            userHandbook.first = first
            try:
                with transaction.atomic():
                    userHandbook.save()
            except IntegrityError:
                pass

    if len(list(set(newDocIds) - set(preDocIds))) > 0:
        newDocNotificationByUserGroup(user_id)
    print("Handbook was saved by user")

def deleteHandbookByGroup(group_id):
    relDocs = Document.objects.filter(groups=group_id)
    relUsers = User.objects.filter(groups=group_id)
    
    relHandbooks = UserHandbook.objects.filter(user__in=relUsers, document__in=relDocs)
    for hb in relHandbooks:
        uid = hb.user_id
        uGroups = Group.objects.filter(user=uid).distinct()
        did = hb.document_id
        dGroups = Group.objects.filter(document=did).distinct()

        diff = set(uGroups) - set(dGroups)
        rem = set(uGroups) - set(diff)
        if len(rem) == 1:
            hb.delete()
    
    print("Handbook was deleted by group")