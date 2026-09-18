document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form")
    const password = document.getElementById("inputPassword");
    const rePassword = document.getElementById("inputRePassword");

    function orderPassword() {
        const isValidLength = password.value.length >= 8 && password.value.length <= 30;

        rePassword.disabled = !isValidLength;

        if (!isValidLength) {
            rePassword.value = "";
            rePassword.classList.remove("is-valid", "is-invalid");
        }
    }

    function checkPasswordMatch() {
        if (rePassword.value) {
            if (password.value !== rePassword.value) {
                rePassword.classList.add("is-invalid");
                rePassword.classList.remove("is-valid");
            } else {
                rePassword.classList.add("is-valid");
                rePassword.classList.remove("is-invalid");
            }
        } else {
            rePassword.classList.remove("is-valid", "is-invalid");
        }
    }

    password.addEventListener("input", () => {
        orderPassword();
        checkPasswordMatch();
    });
    rePassword.addEventListener("input", checkPasswordMatch);

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = Object.fromEntries(new FormData(form));

        if (data.password !== data.rePassword) {
            alert("The passwords do not match.");
            return;
        }

        delete data.rePassword;

        try {
            const response = await fetch(window.location.pathname, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const user = await response.json();
                alert(`Thanks, ${user.name}.`)
                window.location.href = "/";
            } else {
                const errorData = await response.json();
                alert (errorData.detail || "Sign-Up Failed");
            }
        } catch (error) {
            console.error("Error: ", error);
            alert("Server Error");
        }
    });
})