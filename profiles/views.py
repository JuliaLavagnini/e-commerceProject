from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Payment

@login_required
def profile(request):
    """ Display the user's profile. """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'payment_reference' in request.POST:  # Check if the cancel button was clicked
            payment_reference = request.POST.get('payment_reference')
            try:
                payment = Payment.objects.get(payment_reference=payment_reference, user=request.user)
                payment.status = 'Cancelled'
                payment.save()
                messages.success(request, 'Payment cancelled successfully')
            except Payment.DoesNotExist:
                messages.error(request, 'Payment not found or you do not have permission to cancel this payment')
            return redirect('profile')
        else:
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('profile')
            else:
                messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile, initial={'username': request.user.username})

    payments = Payment.objects.filter(user=request.user).order_by('-payment_date')

    template = 'profile/profile.html'
    context = {
        'form': form,
        'payments': payments,
    }

    return render(request, template, context)

def purchase_history(request, payment_reference):
    order = get_object_or_404(Payment, payment_reference=payment_reference)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})
