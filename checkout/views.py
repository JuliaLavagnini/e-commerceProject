from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from django.conf import settings

import stripe


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
        
        form = PaymentForm(initial={'plan_name': plan_name, 'plan_price': plan_price})
        context = {
            'form' : form,
            'stripe_public_key' : settings.STRIPE_PUBLIC_KEY,
        }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request):
    # You can render a success page here
    return render(request, 'checkout_success.html')
