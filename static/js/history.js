let currentPage = 1;

const pageSize = 10;

function formatDate(dateString){

    const date = new Date(dateString);

    return date.toLocaleString(

        "en-IN",

        {
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit",
            hour12: true
        }
    );
}
async function loadHistory(){

    const token =

    localStorage.getItem(
        "token"
    );

    if(!token){

        window.location.href =
        "/login-page";

        return;
    }

    const response =

    await fetch(

        `/history?page=${currentPage}&page_size=${pageSize}`,

        {

            headers: {

                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    const responseData =await response.json();

    document.getElementById(
        "welcomeUser"
    ).innerText =`Welcome, ${responseData.username}`;

    const data =responseData.history;

    let tableHtml =
    `
    <table>

        <tr>
          
            <th>AQI</th>
            <th>Category</th>
            <th>Confidence</th>
            <th>Date</th>

        </tr>
    `;

    data.forEach(

        record => {

            tableHtml +=

            `
            <tr>
                <td>${record.AQI}</td>
                <td>
                    ${record.predicted_category}
                </td>
                <td>
                    ${record.confidence}%
                </td>
                <td>
                    ${formatDate(record.created_at)}
                </td>

            </tr>
            `;
        }
    );

    tableHtml +="</table>";
    document.getElementById(
        "historyTable"
    ).innerHTML =tableHtml;
    document.getElementById(
        "pageNumber"
    ).innerText =`Page ${currentPage}`;
}

loadHistory();

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

function nextPage(){

    console.log("Next clicked");

    currentPage++;

    console.log("Current Page:", currentPage);

    loadHistory();
}

function previousPage(){

    console.log("Previous clicked");

    if(currentPage > 1){

        currentPage--;

        console.log("Current Page:", currentPage);

        loadHistory();
    }
}