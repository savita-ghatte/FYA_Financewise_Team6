function loginUser() {

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please enter both email and password.");
        return;
    }

    fetch("http://127.0.0.1:5000/login", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email,
            password: password
        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.success) {

            // Redirect after successful login
            window.location.href = "dashboard.html";

        }

    })

    .catch(error => {

        alert("Unable to connect to the server.");

    });

}
function handleForgotPassword(event) {
    event.preventDefault();
    
    // Check if the user already typed their email in the login box
    let email = document.getElementById("email").value;

    // If empty, prompt them to enter it
    if (!email) {
        email = prompt("Please enter your registered email address to reset your password:");
    }

    if (!email) {
        return; // User cancelled the prompt
    }

    fetch("http://127.0.0.1:5000/forgot-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert("Unable to connect to the server.");
    });
}