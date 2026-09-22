document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form") as HTMLFormElement;

    function syncPasswordValidity() {
        const password = document.getElementById("inputPassword") as HTMLInputElement;
        const rePassword = document.getElementById("inputRePassword") as HTMLInputElement;

        const isPasswordValid = password.value.length >= 8 && password.value.length <= 30;
        rePassword.disabled = !isPasswordValid;

        if (!isPasswordValid) {
            rePassword.value = "";
            rePassword.classList.remove("is-valid", "is-invalid");
            return;
        }

        if (password.value !== rePassword.value) {
            rePassword.setCustomValidity("Passwords do not match");
        } else {
            rePassword.setCustomValidity("");
        }
    }

    form.querySelectorAll("input").forEach((input: HTMLInputElement) => {
        input.addEventListener("input", () => {
            if (input.id.toLowerCase().includes("password")) {
                syncPasswordValidity();
            }
            applyAutoStyle(input);
        });
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        syncPasswordValidity();

        if (!form.checkValidity()) {
            form.querySelectorAll("input").forEach(applyAutoStyle);

            const firstInvalid = form.querySelector(":invalid") as HTMLElement;
            if (firstInvalid) {
                firstInvalid.focus();
            }
            return;
        }

        const data = Object.fromEntries(new FormData(form));

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
                alert(errorData.detail || "Registration failed.");
            }
        } catch (error) {
            console.error("Error: ", error);
            alert("Server Connection Error");
        }
    });
});