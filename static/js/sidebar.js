document.addEventListener(

    "DOMContentLoaded",

    function(){

        const role =
        localStorage.getItem(
            "role"
        );

        const adminBtn =
        document.getElementById(
            "adminBtn"
        );

        if(
            role === "admin" &&
            adminBtn
        ){

            adminBtn.style.display =
            "block";
        }
    }
);

function goToUsers(){

    window.location.href =
    "/users-page";
}