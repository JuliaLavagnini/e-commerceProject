from django.shortcuts import render
from .models import Plan

# Create your views here.
def plans(request):
    plans = Plan.objects.all()
    return render(request, 'plans/plans.html', {'plans': plans})