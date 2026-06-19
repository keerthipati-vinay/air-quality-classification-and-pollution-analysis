const username =
localStorage.getItem(
    "username"
);

if(username){

    document.getElementById(
        "welcomeBanner"
    ).innerText =
    `Welcome Back, ${username}`;
}
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