var password = document.getElementById("password_input")
  , confirm_password = document.getElementById("conf_password");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;




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
