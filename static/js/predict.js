// VALIDATE INPUT VALUES

function validateValue(value, fieldName) {

if (isNaN(value) || value < 0) {

    throw new Error(
        `${fieldName} must be a positive number`
    );
}

return value;

}

document.addEventListener(

    "DOMContentLoaded",

    function(){

        document.getElementById(
            "resultSection"
        ).style.display = "none";
    }
);

// PREDICTION FORM

document
.getElementById("predictForm")
.addEventListener("submit", async function (e) {

    e.preventDefault();

    try {

        const token = localStorage.getItem("token");

        if (!token) {

            alert("Please login first");

            window.location.href = "/login-page";

            return;
        }

        const inputData = {

            PM2_5: validateValue(
                parseFloat(document.getElementById("PM2_5").value),
                "PM2.5"
            ),

            PM10: validateValue(
                parseFloat(document.getElementById("PM10").value),
                "PM10"
            ),

            NO: validateValue(
                parseFloat(document.getElementById("NO").value),
                "NO"
            ),

            NO2: validateValue(
                parseFloat(document.getElementById("NO2").value),
                "NO2"
            ),

            NOx: validateValue(
                parseFloat(document.getElementById("NOx").value),
                "NOx"
            ),

            NH3: validateValue(
                parseFloat(document.getElementById("NH3").value),
                "NH3"
            ),

            CO: validateValue(
                parseFloat(document.getElementById("CO").value),
                "CO"
            ),

            SO2: validateValue(
                parseFloat(document.getElementById("SO2").value),
                "SO2"
            ),

            O3: validateValue(
                parseFloat(document.getElementById("O3").value),
                "O3"
            ),

            Benzene: validateValue(
                parseFloat(document.getElementById("Benzene").value),
                "Benzene"
            ),

            Toluene: validateValue(
                parseFloat(document.getElementById("Toluene").value),
                "Toluene"
            ),

            Xylene: validateValue(
                parseFloat(document.getElementById("Xylene").value),
                "Xylene"
            ),

            AQI: validateValue(
                parseFloat(document.getElementById("AQI").value),
                "AQI"
            )
        };

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify(inputData)
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Prediction Failed"
            );
        }
        

        // DISPLAY PREDICTION

        const predictionElement =document.getElementById("prediction");
        predictionElement.innerText = "Prediction : " +data.predicted_category;

         // Change color based on category

        switch(data.predicted_category){

            case "Good":

                predictionElement.style.color =
                "#16a34a"; // Green
            break;

            case "Satisfactory":

                predictionElement.style.color =
                "#65a30d"; // Light Green
            break;

            case "Moderate":

                predictionElement.style.color =
                "#eab308"; // Yellow
            break;

            case "Poor":

                predictionElement.style.color =
                "#f97316"; // Orange
            break;

            case "Very Poor":

                predictionElement.style.color =
                "#dc2626"; // Red
            break;

            case "Severe":

                predictionElement.style.color =
                "#7f1d1d"; // Dark Red
            break;

            default:

                predictionElement.style.color =
            "#2563eb";
        }
        let recommendation = "";
        const recommendationElement =document.getElementById("recommendation");
       

        switch(data.predicted_category){

            case "Good":

                recommendation =
                "Air quality is good. Outdoor activities can be enjoyed without any special precautions.";
            break;

            case "Satisfactory":

                recommendation =
                "Air quality is acceptable. Most people can continue normal outdoor activities.";
            break;

            case "Moderate":

                recommendation =
                "Sensitive individuals should limit prolonged outdoor exposure and monitor symptoms.";
            break;

            case "Poor":

                recommendation =
                "Reduce outdoor activities and consider wearing a mask when spending time outside.";
            break;

            case "Very Poor":

                recommendation =
                "Avoid unnecessary outdoor exposure and use a protective mask when going outside.";
            break;

            case "Severe":

                recommendation =
                "Stay indoors as much as possible and wear an N95 mask if outdoor travel is unavoidable.";
            break;

            default:

                recommendation =
                "No recommendation available.";
        }
        recommendationElement.innerText =recommendation;

        document.getElementById(
            "confidence"
        ).innerText =
            "Confidence : " +
            data.confidence +
            "%";

        // DISPLAY CLASS PROBABILITIES

        let probabilityHtml =
            "<h3>Class Probabilities</h3>";

        probabilityHtml +=
            "<table border='1' cellpadding='8'>";

        probabilityHtml +=
            "<tr><th>Category</th><th>Probability (%)</th></tr>";

        for (
            const category
            in
            data.all_classes_probabilities
        ) {

            probabilityHtml += `
                <tr>
                    <td>${category}</td>
                    <td>${data.all_classes_probabilities[category]}</td>
                </tr>
            `;
        }

        probabilityHtml += "</table>";

        document.getElementById(
            "probabilities"
        ).innerHTML =
            probabilityHtml;
       
        document.getElementById(
            "resultSection"
        ).style.display =
            "block";
    }

    catch (error) {

        alert(
            error.message
        );
    }
});

// FUNCTIONS
function goToLanding(){

    window.location.href =
    "/landing-page";
}

function goToDashboard(){

    window.location.href =
    "/dashboard";
}

function goToPredict(){

    window.location.href =
    "/predict-page";
}

function goToHistory(){

    window.location.href =
    "/history-page";
}

function logout(){

    localStorage.removeItem(
        "token"
    );

    window.location.replace(
        "/login-page"
    );
}
function clearForm(){

    document.getElementById(
        "predictForm"
    ).reset();

    document.getElementById(
        "prediction"
    ).innerText = "";

    document.getElementById(
        "confidence"
    ).innerText = "";

    document.getElementById(
        "probabilities"
    ).innerHTML = "";

    document.getElementById(
        "recommendation"
    ).innerText = "";

    document.getElementById(
        "resultSection"
    ).style.display =
    "none";
}

document.addEventListener(

    "DOMContentLoaded",

    function(){

        document
        .querySelectorAll(
            'input[type="number"]'
        )
        .forEach(input => {

            input.addEventListener(

                "input",

                function(){

                    if(this.value < 0){

                        this.value = 0;
                    }
                }
            );
        });
    }
);