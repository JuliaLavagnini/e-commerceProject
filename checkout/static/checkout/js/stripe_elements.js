$(document).ready(function() {
    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);
    console.log(clientSecret);
    console.log(stripePublicKey);
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

    // Handle realtime validation errors on the card element
    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submit
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        card.update({ 'disabled': true});
        $('#submit-button').attr('disabled', true);

        // From using {% csrf_token %} in the form
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
        };
        var url = '/checkout/cache_checkout_data/';
        
        $.post(url, postData).done(function () {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        email: $.trim(form.email.value),
                        address:{
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            state: $.trim(form.county.value),
                        }
                    }
                }
            }).then(function(result) {
                    if (result.error) {
                        var errorDiv = document.getElementById('card-errors');
                        var html = `
                            <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>`;
                        $(errorDiv).html(html);
                        $('#payment-form').fadeToggle(100);
                        card.update({ 'disabled': false});
                        $('#submit-button').attr('disabled', false);
                    } else {
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });
        }).fail(function () {
            // just reload the page, the error will be in django messages
            location.reload();
        })
    });
});