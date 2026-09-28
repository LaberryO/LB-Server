document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form") as HTMLFormElement;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const data = Object.fromEntries(new FormData(form));

        try {
            const response = await fetch("", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${data.token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "messagebaseId": "SS000000",
                    "callback": "",
                    "header": "0",
                    "recvInfoList": [
                        {   
                            "clikey": "test01",
                            "phone": data.phone,
                            "mergeData": {
                                "title": data.title,
                                "description": data.content
                            }
                        }
                    ]
                })
            });

            if (response.ok) {
                console.log(await response.json());
                alert("Complete. check the console.")
            } else {
                console.log(await response.json());
                alert("Failed. check the console.")
            }
        } catch (error) {
            console.error("Error: ", error);
            alert("Server Connection Error");
        }
    });
});