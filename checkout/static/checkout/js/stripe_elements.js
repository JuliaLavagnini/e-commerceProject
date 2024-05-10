var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
document.querySelector("button").disabled = true;

if (document.getElementById('card-element')) {
    let elements = stripe.elements();

    // Card Element styles
    let style = {
        base: {
            color: "#32325d",
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
                color: "#aab7c4"
            }
        },
        invalid: {
            color: "#fa755a",
            iconColor: "#fa755a"
        }
    };

    card = elements.create('card', { style: style });

    card.mount('#card-element');

    card.on('focus', function () {
        let el = document.getElementById('card-errors');
        el.classList.add('focused');
    });

    card.on('blur', function () {
        let el = document.getElementById('card-errors');
        el.classList.remove('focused');
    });

    card.on('change', function (event) {
        displayError(event);
    });
}

// Function to display error message
function displayError(event) {
    let displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
}

// Import Stripe.js library
import { loadStripe } from '@stripe/stripe-js';

// Initialize Stripe.js with publishable key
const stripePromise = loadStripe(stripePublicKey);

document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('payment-form');
    
    paymentForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const stripe = await stripePromise;

        // Collect form data
        const formData = new FormData(paymentForm);
        const planId = formData.get('plan_id');
        const csrfToken = formData.get('csrfmiddlewaretoken');

        // Make AJAX request to create PaymentIntent
        const response = await fetch('/create_payment_intent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ plan_id: planId }),
        });

        const data = await response.json();

        // Handle response from server
        if (data.client_secret) {
            // Use client_secret to confirm the payment
            const result = await stripe.confirmCardPayment(data.client_secret, {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: formData.get('cardholder_name'),
                    },
                },
            });

            // Handle payment result
            if (result.error) {
                // Display error to user
                console.error(result.error.message);
            } else {
                // Payment successful
                console.log('Payment successful:', result.paymentIntent);
                // Redirect to success page or perform other actions
            }
        } else {
            // Error occurred or client_secret not received
            console.error('Error:', data.message);
        }
    });
});
