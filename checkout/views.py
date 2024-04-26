from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment

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

        # If plan details are not provided, display an error message and redirect
        if not (plan_id and plan_name and plan_price and plan_duration):
            messages.error(request, 'Error: Please select a plan and try again.')
            return redirect('plans')
        
        # Initialize the payment form with the plan details
        form = PaymentForm(initial={
            'plan_name': plan_name,
            'plan_price': plan_price,
            'plan_duration': plan_duration
        })

        context = {
            'form': form,
            'stripe_public_key': 'pk_test_51P9xwZHvKRR9IWdakeWyNYtsqIITfdUSxn1cSVIkNCDvuXnC0A64sTIi8gfegVlg6D77zA4NGbOGnvGNZq7JHOij00RhMVWRSI',
            'client_secret': 'test',
        }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request):
    # You can render a success page here
    return render(request, 'checkout_success.html')
