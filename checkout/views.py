from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.contrib import messages
from django.conf import settings

from .forms import PaymentForm
from .models import PurchaseHistory
from .models import Payment
from plans.models import Plan
from profiles.models import UserProfile

import json
from django.http import JsonResponse
from django.views.generic import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    stripe_public_view = settings.STRIPE_PUBLIC_KEY
    stripe_secret_view = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form_data = {
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'email': request.user.email,
        }
        payment_form = PaymentForm(form_data)

        if payment_form.is_valid():
            # Process the form data and save it to the database
            payment = payment_form.save(commit=False)
            payment.user = request.user
            payment.save()
            
            # Redirect to a success page or another view
            return redirect(reverse('checkout_success', args=[payment.payment_reference]))
    else:
        # Fetch user profile data if available
        profile = UserProfile.objects.filter(user=request.user).first()

        if not profile:
            # Display an error message and redirect the user back to the profile page
            messages.error(request, 'Error: Please complete your profile information.')
            return redirect('profile')
        
        initial_data = {
            'plan_name': request.GET.get('plan_name'),
            'plan_price': request.GET.get('plan_price'),
            'plan_duration': request.GET.get('plan_duration'),
            'country': profile.country,
            'postcode': profile.postcode,
            'town_or_city': profile.town_or_city,
            'street_address1': profile.street_address1,
            'street_address2': profile.street_address2,
            'county': profile.county,
            'email': request.user.email,  # Set the initial email value
        }
        form = PaymentForm(initial=initial_data)
        
        # Check if plan details are passed in the query parameters
        plan_price = request.GET.get('plan_price')
        if not plan_price:
            messages.error(request, 'Error: Please select a plan and try again.')
            return redirect('plans')
        
        price = int(plan_price)
        stripe_total = round(price * 100)
        stripe.api_key = stripe_secret_view
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(intent)

    if not stripe_public_view:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your enviroment?')
        
    context = {
        'form' : form,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY,
        'client_secret' : intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, payment_reference):
    reference = get_object_or_404(Payment, payment_reference=payment_reference)
    # Retrieve payment history for the current user

    context = {
        'reference' : reference, 
    }
    return render(request, 'checkout/includes/checkout_success.html', context)

def checkout_error(request):
    return render(request, 'checkout/includes/checkout_error.html')

