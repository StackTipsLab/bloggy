function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailPattern.test(email);
}


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('subscription-form');
    if (null == form) return;

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        // const name = nameInput.value;
        const email = emailInput.value;

        if (!validateEmail(email)) {
            emailInput.classList.add('is-invalid');
            return;
        } else {
            emailInput.classList.remove('is-invalid');
        }

        const subscriptionData = {
            is_active: true, name: document.getElementById('name').value, email: document.getElementById('email').value
        };

        fetch('/api/1.0/newsletter/subscribe', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }, body: JSON.stringify(subscriptionData)
        })
            .then(response => response.json())
            .then(data => {
                showToast('Subscription successful! Thank you for subscribing.', "success")
                form.reset();
            })
            .catch(error => {
                showToast('Subscription failed. Please try again later.', "error")
            });
    });
});
