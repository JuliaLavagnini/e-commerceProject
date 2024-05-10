from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import PurchaseHistory

@login_required
def profile_view(request):
    # Retrieve the current user's information
    user_info = request.user
    
    # Retrieve the purchase history for the current user
    purchase_history = PurchaseHistory.objects.filter(user=request.user)
    
    context = {
        'user_info': user_info,
        'purchase_history': purchase_history,
    }
    return render(request, 'profile/profile.html', context)