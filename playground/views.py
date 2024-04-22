from django.shortcuts import render
from django.http import HttpResponse

# request -> response
def index(request):
    return render(request, 'index.html')