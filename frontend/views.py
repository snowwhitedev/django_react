from django.shortcuts import render

from django.views.generic.detail import DetailView

# from .models import Todo

# from todos.models import Todo

def index(request):
    return render(request, 'frontend/index.html')

def policy(request):
    return render(request, 'frontend/index.html')

def repetition(request):
    return render(request, 'frontend/index.html')

def users(request):
    return render(request, 'frontend/index.html')
# class TodoDetailView(DetailView):
#     model = Todo
#     template_name = 'frontend/index.html'
