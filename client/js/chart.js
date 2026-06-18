let chartInstance = null;

function initChart(history) {

    const categoriesMap = {
        "1h": ["-55m", "-45m", "-35m", "-25m", "-15m", "-5m", "Now"],
        "1d": ["0h", "4h", "8h", "12h", "16h", "20h", "24h"],
        "1w": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "1m": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "1y": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    };

    function renderChart(range = "1w") {

        const data = history?.[range] || {
            latency: [120, 130, 110, 140, 115, 125, 130],
            availability: [100, 99, 100, 100, 100, 99, 100],
            errors: [0, 1, 0, 0, 0, 1, 0]
        };

        const options = {
            chart: {
                type: "line",
                height: 350,
                toolbar: {
                    show: false
                }
            },

            series: [
                {
                    name: "Latency (ms)",
                    data: data.latency
                },
                {
                    name: "Availability (%)",
                    data: data.availability
                },
                {
                    name: "Errors",
                    data: data.errors
                }
            ],

            colors: ["#3B82F6", "#22C55E", "#EF4444"],

            stroke: {
                curve: "smooth",
                width: 3
            },

            xaxis: {
                categories: categoriesMap[range]
            },

            tooltip: {
                shared: true,
                intersect: false
            },

            grid: {
                strokeDashArray: 4
            }
        };

        if (chartInstance) {
            chartInstance.updateOptions(options);
        } else {
            chartInstance = new ApexCharts(
                document.querySelector("#line-chart"),
                options
            );

            chartInstance.render();
        }
    }

    // Initial chart
    renderChart("1w");

    // Timeline buttons
    document.querySelectorAll(".timeline-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            renderChart(btn.dataset.range);
        });
    });
}