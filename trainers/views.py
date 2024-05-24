from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Trainer
from .forms import TrainerForm

# Create your views here.
from .models import Trainer

def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainers.html', {'trainers': trainers})

def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    return render(request, 'trainers/trainer_detail.html', {'trainer': trainer})

@login_required
def add_trainer(request):
    """ Add a trainer """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save()
            messages.success(request, 'Successfully added trainer!')
            return redirect(reverse('trainer'))
        else:
            messages.error(request,
                           ('Failed to add trainer. '
                            'Please ensure the form is valid.'))
    else:
        form = TrainerForm()

    template = 'trainers/add_trainer.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_trainer(request, trainer_id):
    """ Edit a trainer """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    trainer = get_object_or_404(Trainer, pk=trainer_id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated trainer!')
            return redirect(reverse('trainer'))
        else:
            messages.error(request,
                           ('Failed to update trainer. '
                            'Please ensure the form is valid.'))
    else:
        form = TrainerForm(instance=trainer)
        messages.info(request, f'You are editing {trainer.name}')

    template = 'trainers/edit_trainer.html'
    context = {
        'form': form,
        'trainer': trainer,
    }

    return render(request, template, context)

@login_required
def delete_trainer(request, trainer_id):
    """ Delete a trainer """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    trainer = get_object_or_404(Trainer, pk=trainer_id)
    trainer.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('trainers'))