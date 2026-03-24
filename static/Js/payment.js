// static/js/payment.js

function buyCourse(courseId) {
    alert("Processing payment...");

    fetch(`/buy/${courseId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Payment successful 🎉");
            window.location.href = "/my-courses/";
        } else {
            alert("Payment failed ❌");
        }
    });
}

// CSRF helper
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        .split('=')[1];
}