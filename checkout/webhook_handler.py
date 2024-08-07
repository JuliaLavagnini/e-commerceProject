from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Payment
from profiles.models import UserProfile

import json
import time
import stripe

class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, payment):
        """Send the user a confirmation email"""
        cust_email = payment.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'payment': payment})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'payment': payment, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        intent = event.data.object
        pid = intent.id

        metadata = intent.metadata
        plan_name = metadata.get('plan_name')
        plan_price = metadata.get('plan_price')
        plan_duration = metadata.get('plan_duration')

        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = stripe_charge.billing_details
        grand_total = round(stripe_charge.amount / 100, 2) 

        profile = None
        username = metadata.get('username')
        if username and username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)

        payment_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                payment = Payment.objects.get(
                    plan_name=plan_name,
                    plan_price=plan_price,
                    plan_duration=plan_duration,
                    email__iexact=billing_details.email,
                    country__iexact=billing_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    stripe_pid=pid,
                )
                payment_exists = True
                break
            except Payment.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if payment_exists:
            self._send_confirmation_email(payment)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified payment already in database'),
                status=200)
        else:
            payment = None
            try:
                payment = Payment.objects.create(
                    plan_name=plan_name,
                    plan_price=plan_price,
                    plan_duration=plan_duration,
                    user_profile=profile,
                    email=billing_details.email,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    stripe_pid=pid,
                )
            except Exception as e:
                if payment:
                    payment.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        
        self._send_confirmation_email(payment)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created payment in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
