
document.getElementById("signup-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("signup-form")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/signup', {
        method: 'POST',
        body: formData
    });

    console.log(response)

    const result = await response.json()
    console.log(result)
});
