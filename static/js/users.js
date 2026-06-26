checkAuth()
let currentPage = 1;

const pageSize = 10;
async function loadUsers(){

    const token =
    localStorage.getItem("token");

    const response =
    await fetch(
        `/users?page=${currentPage}&page_size=${pageSize}`,
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

    const responseData = await response.json();
    const users = responseData.users;

    let html =

    `
    <table>

        <tr>

            <th>ID</th>

            <th>Username</th>

            <th>Email</th>

            <th>Role</th>

            <th>Actions</th>

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

            <td>

                <select
                    onchange="handleAction(this.value, ${user.id})"
                >

                    <option value="">
                        Actions
                    </option>

                    ${
                        user.role === "user"

                        ?

                        `
                        <option value="admin">
                            Make Admin
                        </option>
                        `

                        :

                        `
                        <option value="user">
                            Make User
                        </option>
                        `
                    }

                    <option value="delete">
                        Delete User
                    </option>

                </select>

            </td>

        </tr>
        `;
    });

    html +=
    "</table>";

    document.getElementById(
        "usersTable"
    ).innerHTML =
    html;
    document.getElementById(
        "pageNumber"
    ).innerText =
    `Page ${responseData.page} of ${responseData.total_pages}`;
}

loadUsers();

async function handleAction(action,id){

    if(action === ""){

        return;
    }

    if(action === "admin"){

        await updateRole(id,"admin");
    }

    else if(action === "user"){

        await updateRole(id,"user");
    }

    else if(action === "delete"){

        await deleteUser(id);
    }

}



async function updateRole(id,role){

    const token =
    localStorage.getItem("token");

    const response =
    await fetch(

        `/users/${id}/role`,

        {

            method:"PUT",

            headers:{

                "Authorization":
                `Bearer ${token}`,

                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                role:role
            })
        }
    );

    const data =
    await response.json();

    alert(data.message);

    loadUsers();
}



async function deleteUser(id){

    if(!confirm(
        "Delete this user?"
    )){

        return;
    }

    const token =
    localStorage.getItem("token");

    const response =
    await fetch(

        `/users/${id}`,

        {

            method:"DELETE",

            headers:{

                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    const data =
    await response.json();

    alert(data.message);

    loadUsers();
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

function goToUsers(){

    window.location.href =
    "/users-page";
}

function logout(){

    localStorage.clear();

    history.replaceState(null, "", "/login-page");

    window.location.replace("/login-page");

}

function nextPage(){

    currentPage++;

    loadUsers();

}

function previousPage(){

    if(currentPage > 1){

        currentPage--;

        loadUsers();

    }
}