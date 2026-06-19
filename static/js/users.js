async function loadUsers(){

    const token =
    localStorage.getItem(
        "token"
    );

    const response =
    await fetch(

        "/users",

        {
            headers:{
                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    if(!response.ok){

        alert(
            "Admin Access Required"
        );

        return;
    }

    const users =
    await response.json();

    let html =

    `
    <table>

        <tr>

            <th>ID</th>

            <th>Username</th>

            <th>Email</th>

            <th>Role</th>

        </tr>
    `;

    users.forEach(user => {

        html +=

        `
        <tr>

            <td>${user.id}</td>

            <td>${user.username}</td>

            <td>${user.email}</td>

            <td>${user.role}</td>

        </tr>
        `;
    });

    html +=
    "</table>";

    document.getElementById(
        "usersTable"
    ).innerHTML =
    html;
}

loadUsers();

function goToDashboard(){

    window.location.href =
    "/dashboard";
}

function goToUsers(){

    window.location.href =
    "/users-page";
}

function logout(){

    localStorage.removeItem(
        "token"
    );

    localStorage.removeItem(
        "role"
    );

    window.location.href =
    "/login-page";
}