from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('plan_name', 'plan_price', 'plan_duration',)
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'plan_name': 'Plan Name',
            'plan_price': 'Plan Price',
            'plan_duration': 'Plan Duration',
        }
   