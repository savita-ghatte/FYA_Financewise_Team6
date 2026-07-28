function registerUser() {

    let fullname = document.getElementById("fullname").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    let dob = document.getElementById("dob").value;
    let age = document.getElementById("age").value;

    let gender = document.getElementById("gender").value;
    let occupation = document.getElementById("occupation").value;

    let goal = document.getElementById("goal").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    fetch("http://127.0.0.1:5000/signup", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            fullname: fullname,
            email: email,
            password: password,
            dob: dob,
            age: age,
            gender: gender,
            occupation: occupation,
            goal: goal

        })

    })

    .then(response => response.json())

    .then(data => {

        alert(data.message);

        if (data.success) {
            window.location.href = "login.html";
        }

    })

    .catch(error => {

        alert("Server Error");

    });

}