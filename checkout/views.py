from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .forms import PaymentForm
from .models import PurchaseHistory
from plans.models import Plan

import json
from django.http import JsonResponse
from django.views.generic import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            payment = form.save(commit=False)
            payment.user = request.user  # Assuming you have authentication set up
            payment.save()
            
            # Redirect to a success page or another view
            return redirect('checkout_success')
    else:
        # Check if plan details are passed in the query parameters
        plan_id = request.GET.get('plan_id')
        plan_name = request.GET.get('plan_name')
        plan_price = request.GET.get('plan_price')
        plan_duration = request.GET.get('plan_duration')



        # Check if a plan ID is provided in the query parameters
        plan_id = request.GET.get('plan_id')
        if not plan_id:
            # Display an error message and redirect the user back to the plans page
            messages.error(request, 'Error: Please select a plan and try again.')
            return redirect('plans')
        
        form = PaymentForm(initial={'plan_name': plan_name, 'plan_price': plan_price, 'plan_duration' : plan_duration})
        
    context = {
        'form' : form,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request):
    # Retrieve payment history for the current user
    payment_history = PurchaseHistory.objects.filter(user=request.user).order_by('-payment_date')

    context = {
        'payment_history': payment_history,
    }

    return render(request, 'checkout/includes/checkout_success.html', context)

def checkout_error(request):
    return render(request, 'checkout/includes/checkout_error.html')

class StripePaymentView(View):
    def post(self, request, *args, **kwargs):
        try:
            plan_id = request.POST.get('plan_id')
            plan = Plan.objects.get(pk=plan_id)
            amount = plan.plan_price * 100  # Convert to pennies

            # Continue with payment processing...
            # This part depends on your payment processing logic using Stripe

            return redirect('checkout_success')

        except Plan.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid plan'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        
