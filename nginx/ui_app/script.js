const API_ENDPOINT = "http://localhost:8000/";

document.querySelector('.submit_button').addEventListener('click', function(event) {
    event.preventDefault();
    submitUserForm();
});
//Pobieranie danych z formularzu
function collectUserInfo() {
    return {
        firstName: document.getElementById("first_name_input").value.trim(),
        lastName: document.getElementById("last_name_input").value.trim(),
        role: document.getElementById("role_input").value.trim(),
        privacyAccepted: document.getElementById("privacy_policy_input").checked
    };
}

//Wysłanie formularza 
async function submitUserForm() {
    const userInfo = collectUserInfo();

    const errorMessage = validateUserInfo(userInfo);
    if (errorMessage) {
        alert(errorMessage);
        return;
    }

    if (!checkPrivacyPolicy(userInfo.privacyAccepted)) {
        return;
    }

    try {
        const response = await makePostRequest(API_ENDPOINT, userInfo);
        const newUserList = await processResponse(response);
        console.log(newUserList);
        renderUsers(newUserList);
    } catch (error) {
        logError(error);
    }
}

//Walidacja danych

function validateUserInfo(userInfo) {
    if (!userInfo.firstName) {
        return "First name cannot be empty.";
    }
    if (!userInfo.lastName) {
        return "Last name cannot be empty.";
    }
    if (!userInfo.role) {
        return "Role cannot be empty.";
    }
    return null;
}

function checkPrivacyPolicy(isAccepted) {
    if (!isAccepted) {
        alert("You must agree to the privacy policy.");
        return false;
    }
    return true;
}

async function makePostRequest(url, data) {
    return await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            firstName: data.firstName,
            lastName: data.lastName,
            role: data.role
        })
    });
}

async function processResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
}

function logError(error) {
    console.error('Error:', error);
}

const USERS_API_URL = "http://localhost:8000/users";

//Tworzenie przycisku usuwania powiązanego z id użytkownika
function createDeleteButton(userId) {
    const deleteBtn = document.createElement("button");
    deleteBtn.classList.add("remove-button");
    deleteBtn.setAttribute("data-id", userId);

    const del_user = document.createElement("span");
    del_user.textContent = "Delete user";

    deleteBtn.appendChild(del_user);

    deleteBtn.addEventListener("click", () => {
        if (confirm("Are you sure you want to delete this user?")) {
            deleteUser(userId, deleteBtn);
        }
    });

    return deleteBtn;
}
// Usuwanie użytkownika
async function deleteUser(userId, button) {
    try {
        const response = await fetch(`${USERS_API_URL}/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: userId })
        });
        if (response.ok) {
            const userElement = button.closest('.users_list');
            userElement.remove(); 
        } else {
            alert('Failed to delete user.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while trying to delete the user.');
    }
}
// Pobieranie użytkowników z bazy
async function fetchUsers() {
    try {
        const response = await axios.get(API_ENDPOINT);
        console.log(response);

        const users = response.data;
        renderUsers(users);
    } catch (error) {
        console.error("Error fetching users:", error);
    }
}
//Renderowanie listy użytkowników  
export function renderUsers(users) {
    const userContainer = document.querySelector(".users_list");
    userContainer.innerHTML = "";

    users.forEach(user => {
        const userElement = createUserElement(user);
        userContainer.appendChild(userElement);
    });
}
//Renderowanie użytkownika
function createUserElement(user) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("users_list");

    const userInfo = getUserInfo(user);
    const deleteButton = createDeleteButton(user.id);

    wrapper.appendChild(userInfo);
    wrapper.appendChild(deleteButton);

    return wrapper;
}
//Uzupełnianie danych użytkownika
function getUserInfo(user) {
    const userContainer = document.createElement("div");

    const userName = document.createElement("div");
    userName.textContent = `${user.first_name} ${user.last_name}`;

    const userRole = document.createElement("div");
    userRole.textContent = user.role;

    userContainer.appendChild(userName);
    userContainer.appendChild(userRole);

    return userContainer;
}

fetchUsers();
