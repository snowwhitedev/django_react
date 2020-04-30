from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from backend.models import PolicyItem
from django.db.models import Max
from backend.actions.admin.policyitem import getPolicyItemTexts

def getMaxPolicyItemId(request):
    maxId = PolicyItem.objects.aggregate(Max('id'))
    # data =  {"id": maxId}
    return JsonResponse(maxId)

def checkValidBody(request):
    docBody = request.GET['docBody']
    res = getPolicyItemTexts(docBody, docId=None)
    valid = True 
    if res == -1:
        valid = False
    response = {"valid": valid}
    return JsonResponse(response)