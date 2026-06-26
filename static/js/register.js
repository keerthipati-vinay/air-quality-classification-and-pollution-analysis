document
.getElementById("registerForm")
.addEventListener(
    "submit",

    async function(e){

        e.preventDefault();

        const username =
        document.getElementById(
            "username"
        ).value.trim();

        const email =
        document.getElementById(
            "email"
        ).value.trim();

        const password =
        document.getElementById(
            "password"
        ).value;

        const confirmPassword =
        document.getElementById(
            "confirmPassword"
        ).value;

        const message =
        document.getElementById(
            "message"
        );

        message.innerText = "";

        // USERNAME VALIDATION

        const usernameRegex =
        /^[a-zA-Z0-9_]{3,20}$/;

        if(
            !usernameRegex.test(
                username
            )
        ){

            message.innerText =
            "Username must be 3-20 characters and contain only letters, numbers and underscore.";

            return;
        }

        // EMAIL VALIDATION

        const emailRegex =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if(
            !emailRegex.test(
                email
            )
        ){

            message.innerText =
            "Enter a valid email address.";

            return;
        }

        // PASSWORD VALIDATION

        const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

        if(
            !passwordRegex.test(
                password
            )
        ){

            message.innerText =
            "Password must contain uppercase, lowercase, number, special character and be at least 8 characters.";

            return;
        }

        // CONFIRM PASSWORD VALIDATION

        if(
            password !==
            confirmPassword
        ){

            message.innerText =
            "Password and Confirm Password do not match.";

            return;
        }

        const userData = {

            username: username,

            email: email,

            password: password
        };

        try{

            const response =
            await fetch(

                "/register",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify(
                        userData
                    )
                }
            );

            const data =
            await response.json();

            message.innerText =
            data.message ||
            data.detail;

            if(response.ok){

                setTimeout(

                    () => {

                        window.location.href =
                        "/login-page";

                    },

                    1500
                );
            }

        }

        catch(error){

            message.innerText =
            "Unable to connect to the server.";

            console.error(error);
        }

    }
);

// PASSWORD TOGGLE

function togglePassword(id){

    const passwordField =

    document.getElementById(id);

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