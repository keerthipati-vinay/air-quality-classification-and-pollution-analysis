async function loadAnalytics() {

    const token =
    localStorage.getItem(
        "token"
    );

    const response =
    await fetch(

        "/analytics",

        {
            headers: {
                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    const data =
    await response.json();

    createTrendChart(
        data.trend
    );

    createCategoryChart(
        data.categories
    );
}

function createTrendChart(
    trend
) {

    new Chart(

        document.getElementById(
            "aqiTrend"
        ),

        {

            type: "line",

            data: {

                labels:
                trend.map(
                    t => t.date
                ),

                datasets: [{

                    label:
                    "AQI Trend",

                    data:
                    trend.map(
                        t => t.aqi
                    ),

                    borderColor:
                    "#14b8a6",

                    backgroundColor:
                    "#14b8a6",

                    borderWidth: 3,

                    tension: 0.4,

                    fill: false
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        display: true,

                        position: "top"
                    },

                    title: {

                        display: true,

                        text:
                        "AQI Trend Over Time",

                        font: {

                            size: 18
                        }
                    }
                },

                scales: {

                    x: {

                        title: {

                            display: true,

                            text: "Date"
                        }
                    },

                    y: {

                        beginAtZero: true,

                        title: {

                            display: true,

                            text:
                            "AQI Value"
                        }
                    }
                }
            }
        }
    );
}

function createCategoryChart(
    categories
) {

    new Chart(

        document.getElementById(
            "categoryChart"
        ),

        {

            type: "bar",

            data: {

                labels:
                Object.keys(
                    categories
                ),

                datasets: [{

                    label:
                    "Prediction Count",

                    data:
                    Object.values(
                        categories
                    ),

                    backgroundColor:
                    "#14b8a6",

                    borderRadius: 8
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        display: true,

                        position: "top"
                    },

                    title: {

                        display: true,

                        text:
                        "Air Quality class Distribution",

                        font: {

                            size: 18
                        }
                    }
                },

                scales: {

                    x: {

                        title: {

                            display: true,

                            text:
                            "Air Quality Category"
                        }
                    },

                    y: {

                        beginAtZero: true,

                        title: {

                            display: true,

                            text:
                            "Prediction Count"
                        }
                    }
                }
            }
        }
    );
}

loadAnalytics();

function goToLanding() {

    window.location.href =
    "/landing-page";
}

function goToDashboard() {

    window.location.href =
    "/dashboard";
}

function goToPredict() {

    window.location.href =
    "/predict-page";
}

function goToHistory() {

    window.location.href =
    "/history-page";
}

function goToAnalytics() {

    window.location.href =
    "/analytics-page";
}

function logout() {

    localStorage.removeItem(
        "token"
    );

    window.location.replace(
        "/login-page");
}