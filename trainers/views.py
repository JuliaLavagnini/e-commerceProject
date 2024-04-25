from django.shortcuts import render, get_object_or_404
from .models import Trainer

# Create your views here.
from .models import Trainer

def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainers.html', {'trainers': trainers})

def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    return render(request, 'trainers/trainer_detail.html', {'trainer': trainer})