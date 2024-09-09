document.getElementById("signup-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("signup-form")
    const formData = new FormData(form);

    const response = await fetch('/signup', {
        method: 'POST', 
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        console.log(result)
    }
});