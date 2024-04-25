from django.shortcuts import render, redirect
from django.conf import settings


def checkout(request):
    plan_id = request.GET.get('plan_id')
    plan_name = request.GET.get('plan_name')
    plan_price = request.GET.get('plan_price')
    plan_type = request.GET.get('plan_type')
    
    context = {
        'plan_name': plan_name,
        'plan_price': plan_price,
        'plan_type': plan_id,
    }

    return render(request, 'checkout/checkout.html',context)