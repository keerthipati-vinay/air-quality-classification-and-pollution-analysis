document
.getElementById("loginForm")
.addEventListener(
    "submit",

    async function(e){

        e.preventDefault();

        const username =
        document.getElementById(
            "username"
        ).value.trim();

        const password =
        document.getElementById(
            "password"
        ).value;

        const message =
        document.getElementById(
            "message"
        );

        message.innerText = "";

        if(username.length < 3){

            message.innerText =
            "Invalid username.";

            return;
        }

        if(password.length < 8){

            message.innerText =
            "Password must be at least 8 characters.";

            return;
        }

        const formData =
        new URLSearchParams();

        formData.append(
            "username",
            username
        );

        formData.append(
            "password",
            password
        );

        const response =
        await fetch(

            "/login",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/x-www-form-urlencoded"
                },

                body: formData
            }
        );

        const data =
        await response.json();
        console.log(data);

        if(response.ok){

            localStorage.setItem(

                "token",

                data.access_token
            );
            localStorage.setItem(
                "username",
                username
            );
            localStorage.setItem(
                "role",
                data.role
            );

            window.location.href =
            "/landing-page";
        }

        else{

            message.innerText =
            data.detail;
        }
    }
);

function togglePassword(){

    const passwordField =

    document.getElementById(
        "password"
    );

    if(
        passwordField.type ===
        "password"
    ){

        passwordField.type =
        "text";
    }

    else{

        passwordField.type =
        "password";
    }
}