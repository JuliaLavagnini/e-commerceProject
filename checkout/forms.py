from django import forms
from .models import Payment
from crispy_forms.layout import Layout, HTML, Row, Column
from crispy_forms.helper import FormHelper

class PaymentForm(forms.ModelForm):
    email = forms.EmailField(disabled=False)

    class Meta:
        model = Payment
        fields = ['plan_name', 'plan_price', 'plan_duration', 'country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'email',
                    css_class='form-group col-md-12 mb-0'
                ), 
                css_class='form-row'
            ),
             Row(
                Column(
                    'street_address1',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'street_address2',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'town_or_city',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'county',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'postcode',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'country',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            
        )
        placeholders = {
            'plan_name': 'Plan Name',
            'plan_price': 'Plan Price',
            'plan_duration': 'Plan Duration',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State',
            'email': 'Email'
        }

        for field in self.fields:
            if field != 'country' and field != 'email':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = False