from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer

from backend.actions.api.auth import signin
from backend.actions.api.handbook import getUserHandbook
from backend.actions.api.handbook import getPolicyItems
from backend.actions.api.handbook import checkPolicyItem
from backend.actions.api.repetition import getUserRepetition, answerUserRepetition
from backend.actions.api.people import getUsers, getUserDocuments

from mindojopolicy.settings import(
    APP_SECRET_KEY
)

class LoginView(APIView):
    def post(self, request):
        headers = request.headers
        userData = {
            "email": request.POST.get('email'),
            'username': request.POST.get('username'),
            'last_name': request.POST.get('last_name'),
            'first_name': request.POST.get('first_name'),
            'gavatar': request.POST.get('gavatar'),
            'appkey': request.POST.get('appkey')
        }
        if not request.POST.get('appkey') == APP_SECRET_KEY:
            response = {
                "code": 400,
                "message": "Please use correct APP key"
            }
            return Response(response)
        response = signin(userData)
        return Response(response)

class HandBookView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        user_id = tokenObj.user_id

        response = getUserHandbook(user_id)
        return Response(response)

class HandbookPolicyView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        user_id = tokenObj.user_id
        document_id = headers['DocumentId']
        response = getPolicyItems(user_id, document_id)
        return Response(response)
    
    def put(self, request, pk, format=None):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        user_id = tokenObj.user_id

        response = checkPolicyItem(user_id, pk)
        return Response(response)
        
class RepetitionView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        user_id = tokenObj.user_id
        response = getUserRepetition(user_id)
        
        return Response(response)
    
    def put(self, request, pk):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        user_id = tokenObj.user_id
        response = answerUserRepetition(pk, request.data['answer'], user_id)
        return Response(response)

class UserView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        admin_id = tokenObj.user_id
        response = getUsers(admin_id)
        return Response(response)

class UserDocumentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        headers = request.headers
        token = headers['Authorization']
        token = token.split(' ')
        token = token[1]
        tokenObj = Token.objects.get(key=token)
        admin_id = tokenObj.user_id
        
        
        response = getUserDocuments(admin_id, request.GET.get('user_id', None))
        return Response(response)

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


        