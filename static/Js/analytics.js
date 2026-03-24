// static/js/analytics.js

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('salesChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar'],
            datasets: [{
                label: 'Sales',
                data: [10, 20, 30]
            }]
        }
    });
});