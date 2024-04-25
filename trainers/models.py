from django.db import models

# Create your models here.
class Trainer(models.Model):
    MORNING = 'morning'
    AFTERNOON = 'afternoon'
    EVENING = 'evening'
    ALL = 'all'

    AVAILABILITY_CHOICES = [
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (EVENING, 'Evening'),
        (ALL, 'All'),
    ]

    FISOTHERAPHY = 'fisiotherapy'
    PRAGNANCE = 'pragnance'
    ACCESSIBILITY = 'accessibility'

    SPECIALLITY_CHOICES = [
        (FISOTHERAPHY, 'Fisiotheraphy'),
        (PRAGNANCE, 'Pragnance'),
        (ACCESSIBILITY, 'Accessibility'),
    ]

    SHORT = 'less_time'
    MID = 'half_time'
    LONG = 'full_time'
    ALL = 'all'

    SESSION_CHOICES = [
        (MID, '30 mins to 45 mins'),
        (LONG, '60 mins or more'),
        (ALL, 'All'),
    ]

    name = models.CharField(max_length=100)
    programs = models.CharField(max_length=50, choices=[('women', 'Women'), ('men', 'Men'), ('children', 'Children'), ('all', 'All')])
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES, default=ALL)
    speciality = models.CharField(max_length=50, choices=SPECIALLITY_CHOICES, default=ALL)
    sessions = models.CharField(max_length=50, choices=SESSION_CHOICES, default=ALL)
    image = models.ImageField(upload_to='trainer_images', default=ALL)


    def __str__(self):
        return self.name