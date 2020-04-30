from backend.models import PolicyItem
from backend.models import Question
from backend.models import RepetitionItem
from backend.models import Document
from backend.models import DocumentStructure
from backend.models import UserHandbook

from backend.actions.notification.notifications import policyitemNotification

CUSTOM_TAG_START = '@POLICYITEM'
CUSTOM_TAG_END = '@ENDPOLICYITEM'

ERROR = -1
SUCCESS = 1

JOINSTRING = ","

def savePolicyItemsByItems(poItems, document):
    # update or save new policy items
    title = document.title
    poItemIds = []
    updatedIds = []
    for item in poItems:
        poItem = PolicyItem()
        poItem.id = item[0]
        poItem.docTitle = title
        poItem.itemText = item[1]
        poItemIds.append(str(item[0]))
        
        prePol = list(PolicyItem.objects.filter(id=item[0]).values('docTitle', 'itemText'))
        if len(prePol) == 0 or not prePol[0]['itemText'] == item[1]: #if policy item is new or changed
            updatedIds.append(str(item[0]))

        poItem.save()
        
                
    # delete old policy items removed from document and repetition
    deleteIds = []
    if not document.policyItems == None:
        prePolicyIds = (document.policyItems).split(JOINSTRING)
        deleteIds = list(set(prePolicyIds) - set(poItemIds))
    
    try:
        deletedPolItems = PolicyItem.objects.filter(id__in=deleteIds)
        deletedPolItems.delete()
        deletedRepItems = RepetitionItem.objects.filter(policy_id__in=deleteIds)
        deletedRepItems.delete()
    except:
        pass
    
    #email notification when one or more items are changed
    if len(updatedIds) > 0:
        policyitemNotification(document)

    poItemIdsStr = JOINSTRING.join(poItemIds)
    description = getDocumentDescription(document.body)
    return (poItemIdsStr, description, updatedIds)

def savePolicyItems(document):
    content = document.body
    title = document.title
    
    poItems = getPolicyItemTexts(content, document.id)
    if poItems is ERROR:
        return False #error

    res = savePolicyItemsByItems(poItems, document)
    return res
    # update or save new policy items
    # poItemIds = []
    # updatedIds = []
    # for item in poItems:
    #     poItem = PolicyItem()
    #     poItem.id = item[0]
    #     poItem.docTitle = title
    #     poItem.itemText = item[1]
    #     poItemIds.append(str(item[0]))
        
    #     prePol = list(PolicyItem.objects.filter(id=item[0]).values('docTitle', 'itemText'))
    #     if len(prePol) == 0 or not prePol[0]['itemText'] == item[1]: #if policy item is new or changed
    #         updatedIds.append(str(item[0]))

    #     poItem.save()
        
                
    # # delete old policy items removed from document and repetition
    # deleteIds = []
    # if not document.policyItems == None:
    #     prePolicyIds = (document.policyItems).split(JOINSTRING)
    #     deleteIds = list(set(prePolicyIds) - set(poItemIds))
    
    # try:
    #     deletedPolItems = PolicyItem.objects.filter(id__in=deleteIds)
    #     deletedPolItems.delete()
    #     deletedRepItems = RepetitionItem.objects.filter(policy_id__in=deleteIds)
    #     deletedRepItems.delete()
    # except:
    #     pass
    
    # #email notification when one or more items are changed
    # if len(updatedIds) > 0:
    #     policyitemNotification(document)

    # poItemIdsStr = JOINSTRING.join(poItemIds)
    # description = getDocumentDescription(content)
    # return (poItemIdsStr, description, updatedIds)  #save success

def savePolicyDocId(pIdStr, docId):
    if len(pIdStr.strip()) == 0:
        return
    pIds = pIdStr.split(',')

    for pId in pIds:
        policyItem = PolicyItem.objects.get(id=pId)
        policyItem.document_id = docId
        policyItem.save()
    

#from document content
def getDocumentDescription(content):
    pos_start = content.find(CUSTOM_TAG_START)
    pos_end = content.rfind(CUSTOM_TAG_END)

    return content[:pos_start] + content[pos_end + len(CUSTOM_TAG_END):]

#from document content
def getPolicyItemTexts(content, docId):
    poItems = []
    content_cpy = content
   
    while(1):
        pos_start = content_cpy.find(CUSTOM_TAG_START)
        if pos_start is -1:
            return poItems
        content_cpy = content_cpy[pos_start + len(CUSTOM_TAG_START):]
        #find id like @POLICYITEM[132]
        if content_cpy[0] != '[':
            return ERROR

        idTagEnd = content_cpy.find(']')
        if idTagEnd is -1:
            return ERROR
        policyId = content_cpy[1: idTagEnd]
        if not policyId.isnumeric():
            return ERROR
        
        policyId = int(policyId)
        #checking colliding policy ids...
        if any( pi[0] == policyId for pi in poItems):
            return ERROR
        
        ds = DocumentStructure.objects.filter(policyitems__id=policyId).values('document_id')
        if len(ds) > 0:
            existingDoc = ds.last()['document_id']
            
            if docId == None: #new document has existing policy item
                return ERROR
            if not int(existingDoc) == int(docId): 
                return ERROR
        
        
        content_cpy = content_cpy[idTagEnd + 1:]

        pos_end = content_cpy.find(CUSTOM_TAG_END)
        if pos_end is -1:
            return ERROR #error
        
        policyText = content_cpy[:pos_end]
        poItems.append([policyId, policyText.strip()])
    
        content_cpy = content_cpy[pos_end + len(CUSTOM_TAG_END):]

#delete by documents
def deletePolicyItemsByDoc(pids):
    policyIds = pids.split(',')
    questions = Question.objects.filter(policyId__in=policyIds)
    questions.delete()
    policies = PolicyItem.objects.filter(id__in=policyIds)
    
    policies.delete()
    return True

def confirmPolicyItems(docBody, docId):
    newItems = getPolicyItemTexts(docBody, docId)

    if newItems == ERROR:
        return False    
    
    document = Document.objects.get(id=docId)
    newItemIds = list(str(item[0]) for item in newItems)
    deleteIds = []
    if not document.policyItems == None:
        prePolicyIds = (document.policyItems).split(JOINSTRING)
        deleteIds = list(set(prePolicyIds) - set(newItemIds))

    removedItems = []
    if len(deleteIds) >0 and not deleteIds[0] == '':
        policies = PolicyItem.objects.filter(id__in=deleteIds).values('id', 'itemText')

        for po in policies:
            questions = Question.objects.filter(policy_id__in=[po['id']]).values('id', 'question', 'answer')
            hbs = UserHandbook.objects.filter(policy_id__in=[po['id']]).values('id')
            rps = RepetitionItem.objects.filter(policy_id__in=[po['id']]).values('id')
            removedItems.append(
                {
                    'policy':{
                        'id': po['id'],
                        'itemText': po['itemText']
                    },
                    'questions': questions,
                    'handbook': hbs,
                    'repetitionItem': rps
                }
            )
    res = {
        "items": newItems,
        "removedItems": removedItems
    }
    return res
    # return removedItems
    
def isValidBody(docBody):

    return True
    
