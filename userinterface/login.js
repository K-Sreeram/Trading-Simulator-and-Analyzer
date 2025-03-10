document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".btnn").addEventListener("click", function (event) {
        event.preventDefault();

        let email = document.querySelector("input[type='email']").value;
        let password = document.querySelector("input[type='password']").value;

        console.log("Button clicked!");  
        console.log("Email:", email);
        console.log("Password:", password);

        if (email === "user@example.com" && password === "password123") {
            window.location.href = "lab1.html"; 
        } else {
            alert("Invalid email or password. Please try again.");
        }
    });
});
