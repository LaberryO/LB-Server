document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form")
    const password = document.getElementById("inputPassword");

    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        const data = Object.fromEntries(new FormData(form));

        
    })
});