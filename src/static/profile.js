document.getElementById("profile-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("profile-form")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/profile', {
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