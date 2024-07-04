from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Plan
from .forms import PlanForm

def plans(request):
    plans = Plan.objects.all()
    return render(request, 'plans/plans.html', {'plans': plans})

@login_required
def add_plan(request):
    """ Add a plan """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save()
            messages.success(request, 'Successfully added plan!')
            return redirect(reverse('plan'))
        else:
            messages.error(request,
                           ('Failed to add plan. '
                            'Please ensure the form is valid.'))
    else:
        form = PlanForm()

    template = 'plans/add_plan.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_plan(request, plan_id):
    """ Edit a plan """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    plan = get_object_or_404(Plan, pk=plan_id)
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated plan!')
            return redirect(reverse('plans'))
        else:
            messages.error(request,
                           ('Failed to update plan. '
                            'Please ensure the form is valid.'))
    else:
        form = PlanForm(instance=plan)
        messages.info(request, f'You are editing {plan.name}')

    template = 'plans/edit_plan.html'
    context = {
        'form': form,
        'plan': plan,
    }

    return render(request, template, context)


@login_required
def delete_plan(request, plan_id):
    """ Delete a plan """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    plan = get_object_or_404(Plan, pk=plan_id)
    plan.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('plans'))