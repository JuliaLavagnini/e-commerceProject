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
        # Extract plan details from query parameters
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
    return render(request, 'checkout/checkout.html', {'form': form})

def checkout_success(request):
    # You can render a success page here
    return render(request, 'checkout_success.html')
