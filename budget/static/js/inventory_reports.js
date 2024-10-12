document.addEventListener('DOMContentLoaded', function() {
    // Bar chart for Stock vs Sales Quantity
    var ctx = document.getElementById('inventoryChart').getContext('2d');
    var inventoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Stock', 'Sales'],
            datasets: [{
                label: "Quantity",
                data: [daily_stock, daily_sales],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
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

    // Bar chart for Stock vs Sales Price
    var ctxPrice = document.getElementById('inventoryChartPrice').getContext('2d');
    var inventoryChartPrice = new Chart(ctxPrice, {
        type: 'bar',
        data: {
            labels: ['Stock', 'Sales'],
            datasets: [{
                label: "Price",
                data: [daily_stock_price, daily_sales_price],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
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

    // Bar chart for number of items sold for each item
    var salesCtx = document.getElementById('inventorySalesStats').getContext('2d');
    var salesBarChart = new Chart(salesCtx, {
        type: 'bar',
        data: {
            labels: itemNames,  // Provided by the template
            datasets: [{
                label: "Number of Items Sold",
                data: quantitiesSold,  // Provided by the template
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
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

    // Line graph for number of items sold for each item
    var lineCtx = document.getElementById('inventoryLineChart').getContext('2d');
    var lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: itemNames,  // X-axis: item names (provided by the template)
            datasets: [{
                label: 'Quantity Sold',
                data: quantitiesSold,  // Y-axis: quantities sold (provided by the template)
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,  // Add some curve to the line
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Items Sold'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantity'
                    }
                }
            }
        }
    });
});
