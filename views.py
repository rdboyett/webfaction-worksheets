from django.http import HttpResponse
from django.contrib.auth.models import User

def home(request):
    return HttpResponse("Hello from django, try out <a href='/admin/'>/admin/</a>\n")