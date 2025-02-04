
document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('lineChart').getContext('2d');
    var items = {{ items|safe }};
    var counts = {{ counts|safe }};
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: items,
            datasets: [{
                label: 'Product Counts',
                data: counts,
                backgroundColor: 'rgba(106, 90, 205,1)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 0.5
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },

            layout: {
        padding: {
            left: 10,  // Adjust as needed
            right: 10, // Adjust as needed
            top: 10,   // Adjust as needed
            bottom: 10 // Adjust as needed
        }
        },
        scales: {
        x: {
            barPercentage: 0.2, // Adjust the width of the bars
            categoryPercentage: 0.6 // Adjust the space between bars
        }
    }
}});

    var crt = document.getElementById('lineChart2').getContext('2d');
    var products = {{ products|safe }};
    var quantities = {{ quantities|safe }};
    var myChart = new Chart(crt, {
        type: 'bar',
        data: {
            labels: products,
            datasets: [{
                label: 'Products Quantities',
                data: quantities,
                fill: false,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});