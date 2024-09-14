document.getElementById("profile-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("profile-form")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch(`/profile/update-profile`, {
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

document.getElementById("password-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("password-form");
    const formData = new FormData(form);

    console.log([...formData.entries()]);

    const response = await fetch(`/profile/change-password`, {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        console.log(result);
    }
});