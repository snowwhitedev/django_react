from rest_framework import routers
from django.urls import path

from .views import LoginView
from .views import HandBookView
from .views import HandbookPolicyView
from .views import RepetitionView
from .views import UserView
from .views import UserDocumentView

from .views import UserViewSet
from .views import HelloView

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'users')

urlpatterns = [
    # router.urls,
    path('hello/', HelloView.as_view(), name="hello"),
    path('login/', LoginView.as_view(), name="login"),
    path('handbook/', HandBookView.as_view(), name="handbook"),
    path('handbook/policies/', HandbookPolicyView.as_view(), name="handbookpolicy"),
    path('handbook/policies/<int:pk>/', HandbookPolicyView.as_view(), name="handbookpolicy_check"),
    path('repetition/', RepetitionView.as_view(), name="repetition"),
    path('repetition/<int:pk>/', RepetitionView.as_view(), name="repetitionanswer"),
    path('people/', UserView.as_view(), name='people'),
    path('people/documents/', UserDocumentView.as_view(), name="userdocument")
]