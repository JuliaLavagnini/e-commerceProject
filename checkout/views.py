from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from .forms import PaymentForm
from .models import Payment
from profiles.models import UserProfile
import logging

logger = logging.getLogger(__name__)

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'plan_name': request.POST.get('plan_name'),
            'plan_price': request.POST.get('plan_price'),
            'plan_duration': request.POST.get('plan_duration'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=str(e), status=400)
    
@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    intent = None  # Initialize intent to None

    if request.method == 'POST':
        form_data = {
            'plan_name': request.POST.get('plan_name'),
            'plan_price': request.POST.get('plan_price'),
            'plan_duration': request.POST.get('plan_duration'),
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'email': request.user.email,
        }

        # Debugging: Log the form data
        print(f"Form Data: {form_data}")

        try:
            plan_price = float(form_data['plan_price'])
            form_data['plan_price'] = plan_price
        except (ValueError, TypeError) as e:
            print(f"Error converting plan_price: {e}")
            messages.error(request, 'Invalid plan price. Please select a valid plan.')
            return redirect('plans')

        payment_form = PaymentForm(form_data)

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user = request.user
            payment.save()

            # Save the info to the user's profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.default_street_address1 = payment.street_address1
            profile.default_street_address2 = payment.street_address2
            profile.default_town_or_city = payment.town_or_city
            profile.default_postcode = payment.postcode
            profile.default_country = payment.country
            profile.default_county = payment.county
            profile.save()

            print("Payment Reference:", payment.payment_reference)
            return redirect(reverse('checkout_success', args=[payment.payment_reference]))
        else:
            print("Form Errors:", payment_form.errors)
            messages.error(request, 'There was an error with your form. Please double-check your information.')
    else:
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Check if plan details are passed in the query parameters
        plan_id = request.GET.get('plan_id')
        plan_name = request.GET.get('plan_name')
        plan_price = request.GET.get('plan_price')
        plan_duration = request.GET.get('plan_duration')

        # Debugging: Log the query parameters
        print(f"Query Params - plan_id: {plan_id}, plan_name: {plan_name}, plan_price: {plan_price}, plan_duration: {plan_duration}")

        if not plan_id or not plan_name or not plan_price or not plan_duration:
            messages.error(request, 'Error: Incomplete plan details. Please choose a plan and try again.')
            return redirect('plans')

        try:
            plan_price = float(plan_price)
        except (ValueError, TypeError) as e:
            print(f"Error converting plan_price: {e}")
            messages.error(request, 'Invalid plan price. Please select a valid plan.')
            return redirect('plans')

        initial_data = {
            'country': profile.default_country,
            'postcode': profile.default_postcode,
            'town_or_city': profile.default_town_or_city,
            'street_address1': profile.default_street_address1,
            'street_address2': profile.default_street_address2,
            'county': profile.default_county,
            'email': request.user.email,
            'plan_name': plan_name,
            'plan_price': plan_price,
            'plan_duration': plan_duration,
        }
        payment_form = PaymentForm(initial=initial_data)

        stripeTotal = round(plan_price * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripeTotal, 
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'username': request.user.username,
                'plan_name': plan_name,
                'plan_price': str(plan_price),
                'plan_duration': plan_duration,
            },
        )

        print(intent)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    context = {
        'form': payment_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else '',
    }

    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, payment_reference):
    try:
        payment = get_object_or_404(Payment, payment_reference=payment_reference)
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f"Error retrieving payment details: {e}")
        # Log the exception for further investigation
        logger.error("Error retrieving payment details: %s", e)
        return redirect('checkout')

    messages.success(request, f'Order successfully processed! A confirmation email will be sent to {payment.email}.')
    print("Payment Reference:", payment_reference)

    return render(request, 'checkout/checkout_success.html', {'payment': payment})
