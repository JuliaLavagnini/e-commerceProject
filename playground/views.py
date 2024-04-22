from django.shortcuts import render
from django.http import HttpResponse

# request -> response
def home_page(request):
    return render(request, 'home.html')