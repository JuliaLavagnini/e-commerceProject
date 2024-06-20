from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from crispy_forms.layout import Layout, HTML, Row, Column
from crispy_forms.helper import FormHelper

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop the 'user' argument if present
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'username',
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    'email',
                    css_class='form-group col-md-6 mb-0'
                ), 
                css_class='form-row'
            ),
             Row(
                Column(
                    'default_street_address1',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'default_street_address2',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'default_town_or_city',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'default_county',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'default_postcode',
                    css_class='form-group col-md-6 mb-0'
                ), 
                Column(
                    'default_country',
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
        )
        placeholders = {
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'default_country': 'Country',
            'username': 'Username',
            'email': 'Email Address'
        }

        self.fields['default_postcode'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ('border-black '
                                                        'rounded-0 '
                                                        'profile-form-input')
            self.fields[field].label = False

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.username = self.cleaned_data['username']
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile