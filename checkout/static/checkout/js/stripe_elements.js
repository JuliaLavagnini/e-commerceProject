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

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
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
});