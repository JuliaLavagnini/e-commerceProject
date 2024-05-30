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

    messages.info(request, (
        f'This is a past confirmation for order number {payment_reference}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

@login_required
def cancel_membership(request, payment_reference):
    order = get_object_or_404(Payment, payment_reference=payment_reference, user=request.user)
    if request.method == 'POST':
        order.active = False
        order.save()
        messages.success(request, 'Your membership has been cancelled.')
    return redirect('profile')

def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})
