function checkAuth(){

    const token = localStorage.getItem("token");

    if(!token){

        history.pushState(null, "", "/login-page");

        window.location.replace("/login-page");

        return;
    }
}

checkAuth();

window.onpageshow = function () {

    checkAuth();

};