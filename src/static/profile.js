function CustomValidation() {
    this.invalidities = [];
  }
  
  CustomValidation.prototype = {
    getInvalidities: function() {
      return this.invalidities.join('. \n');
    },
    checkInvalidity: function(input) {
      this.invalidities = [];
      var username = document.getElementById('username_input');
      var usernameValidationElements = document.querySelectorAll('label[for="username_input"] li');
  
      if (username.value.length < 6 || username.value.length > 13) {
        usernameValidationElements[0].textContent = 'Username must be 6-13 characters long.';
        usernameValidationElements[0].classList.add('invalid');
        usernameValidationElements[0].style.color = 'red';
      } else {
        usernameValidationElements[0].textContent = 'Username is valid length.';
        usernameValidationElements[0].classList.add('valid');
        usernameValidationElements[0].style.color = 'green';
      }
  
      if (/[^a-zA-Z0-9]/.test(username.value)) {
        usernameValidationElements[1].textContent = 'Username must contain only letters and numbers.';
        usernameValidationElements[1].classList.add('invalid');
        usernameValidationElements[1].style.color = 'red';
      } else {
        usernameValidationElements[1].textContent = 'Username contains valid characters.';
        usernameValidationElements[1].classList.add('valid');
        usernameValidationElements[1].style.color = 'green';
      }
  
      if (/\s/.test(username.value)) {
        usernameValidationElements[2].textContent = 'Username must not contain spaces.';
        usernameValidationElements[2].classList.add('invalid');
        usernameValidationElements[2].style.color = 'red';
      } else {
        usernameValidationElements[2].textContent = 'Username contains no spaces.';
        usernameValidationElements[2].classList.add('valid');
        usernameValidationElements[2].style.color = 'green';
      }
  
      // First name validation
      var firstName = document.getElementById('first_name_input');
      var firstNameValidationElements = document.querySelectorAll('label[for="first_name_input"] li');
  
      if (firstName.value.length < 2 || firstName.value.length > 40) {
        firstNameValidationElements[0].textContent = 'First name must be 2-40 characters long.';
        firstNameValidationElements[0].classList.add('invalid');
        firstNameValidationElements[0].style.color = 'red';
      } else {
        firstNameValidationElements[0].textContent = 'First name has valid length.';
        firstNameValidationElements[0].classList.add('valid');
        firstNameValidationElements[0].style.color = 'green';
      }
  
      if (/[^a-zA-Z ]/.test(firstName.value)) {
        firstNameValidationElements[1].textContent = 'First name must contain only letters.';
        firstNameValidationElements[1].classList.add('invalid');
        firstNameValidationElements[1].style.color = 'red';
      } else {
        firstNameValidationElements[1].textContent = 'First name contains valid characters.';
        firstNameValidationElements[1].classList.add('valid');
        firstNameValidationElements[1].style.color = 'green';
      }
  
      if (/\d/.test(firstName.value)) {
        firstNameValidationElements[2].textContent = 'First name must not contain numbers.';
        firstNameValidationElements[2].classList.add('invalid');
        firstNameValidationElements[2].style.color = 'red';
      } else {
        firstNameValidationElements[2].textContent = 'First name contains no numbers.';
        firstNameValidationElements[2].classList.add('valid');
        firstNameValidationElements[2].style.color = 'green';
      }

      var trimmedFirstName = firstName.value.trim();
      
      if (firstName.value !== trimmedFirstName) {
        firstNameValidationElements[3].textContent = 'First name must not have leading or trailing spaces.';
        firstNameValidationElements[3].classList.add('invalid');
        firstNameValidationElements[3].style.color = 'red';
      } else {
        firstNameValidationElements[3].textContent = 'First name has no leading or trailing spaces.';
        firstNameValidationElements[3].classList.add('valid');
        firstNameValidationElements[3].style.color = 'green';
      }



      
  
      // Last name validation
      var lastName = document.getElementById('last_name_input');
      var lastNameValidationElements = document.querySelectorAll('label[for="last_name_input"] li');
  
      if (lastName.value.length < 2 || lastName.value.length > 40) {
        lastNameValidationElements[0].textContent = 'Last name must be 2-40 characters long.';
        lastNameValidationElements[0].classList.add('invalid');
        lastNameValidationElements[0].style.color = 'red';
      } else {
        lastNameValidationElements[0].textContent = 'Last name has valid length.';
        lastNameValidationElements[0].classList.add('valid');
        lastNameValidationElements[0].style.color = 'green';
      }
  
      if (/[^a-zA-Z]/.test(lastName.value)) {
        lastNameValidationElements[1].textContent = 'Last name must contain only letters.';
        lastNameValidationElements[1].classList.add('invalid');
        lastNameValidationElements[1].style.color = 'red';
      } else {
        lastNameValidationElements[1].textContent = 'Last name contains valid characters.';
        lastNameValidationElements[1].classList.add('valid');
        lastNameValidationElements[1].style.color = 'green';
      }
  
      if (/\s/.test(lastName.value)) {
        lastNameValidationElements[2].textContent = 'Last name must not contain spaces.';
        lastNameValidationElements[2].classList.add('invalid');
        lastNameValidationElements[2].style.color = 'red';
      } else {
        lastNameValidationElements[2].textContent = 'Last name contains no spaces.';
        lastNameValidationElements[2].classList.add('valid');
        lastNameValidationElements[2].style.color = 'green';
      }
  
      var email = document.getElementById('email_input');
      var emailValidationElement = document.querySelector('label[for="email_input"] li:nth-child(1)');
      var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailPattern.test(email.value)) {
        emailValidationElement.textContent = 'Contains a valid email.';
        emailValidationElement.classList.add('valid');
        emailValidationElement.style.color = 'green';
      } else {
        emailValidationElement.textContent = 'Does not contain a valid email.';
        emailValidationElement.classList.add('invalid');
        emailValidationElement.style.color = 'red';
      }

              // Password validation
        var password = document.getElementById('password_input');
        var passwordValidationElements = document.querySelectorAll('label[for="password_input"] li');

        if (password.value.length < 8) {
            passwordValidationElements[0].textContent = 'Password must be at least 8 characters long.';
            passwordValidationElements[0].classList.add('invalid');
            passwordValidationElements[0].style.color = 'red';
        } else {
            passwordValidationElements[0].textContent = 'Password has valid length.';
            passwordValidationElements[0].classList.add('valid');
            passwordValidationElements[0].style.color = 'green';
        }

        if (!/\d/.test(password.value)) {
            passwordValidationElements[1].textContent = 'Password must contain at least one number.';
            passwordValidationElements[1].classList.add('invalid');
            passwordValidationElements[1].style.color = 'red';
        } else {
            passwordValidationElements[1].textContent = 'Password contains a number.';
            passwordValidationElements[1].classList.add('valid');
            passwordValidationElements[1].style.color = 'green';
        }

        if (!/[A-Z]/.test(password.value)) {
            passwordValidationElements[2].textContent = 'Password must contain at least one uppercase character.';
            passwordValidationElements[2].classList.add('invalid');
            passwordValidationElements[2].style.color = 'red';
        } else {
            passwordValidationElements[2].textContent = 'Password contains an uppercase character.';
            passwordValidationElements[2].classList.add('valid');
            passwordValidationElements[2].style.color = 'green';
        }

        if (!/[a-z]/.test(password.value)) {
            passwordValidationElements[3].textContent = 'Password must contain at least one lowercase character.';
            passwordValidationElements[3].classList.add('invalid');
            passwordValidationElements[3].style.color = 'red';
        } else {
            passwordValidationElements[3].textContent = 'Password contains a lowercase character.';
            passwordValidationElements[3].classList.add('valid');
            passwordValidationElements[3].style.color = 'green';
        }

        // Confirm password validation
        var confirmPassword = document.getElementById('conf_password');
        var confirmPasswordValidationElements = document.querySelectorAll('label[for="conf_password"] li');

        if (password.value !== confirmPassword.value) {
            confirmPasswordValidationElements[0].textContent = 'Passwords do not match.';
            confirmPasswordValidationElements[0].classList.add('invalid');
            confirmPasswordValidationElements[0].style.color = 'red';
        } else {
            confirmPasswordValidationElements[0].textContent = 'Passwords match.';
            confirmPasswordValidationElements[0].classList.add('valid');
            confirmPasswordValidationElements[0].style.color = 'green';
        }

        // Password validation
        var password = document.getElementById('password_input');
        var passwordValidationElements = document.querySelectorAll('label[for="password_input"] li');

        if (password.value.length < 8) {
            passwordValidationElements[0].textContent = 'Password must be at least 8 characters long.';
            passwordValidationElements[0].classList.add('invalid');
            passwordValidationElements[0].style.color = 'red';
        } else {
            passwordValidationElements[0].textContent = 'Password has valid length.';
            passwordValidationElements[0].classList.add('valid');
            passwordValidationElements[0].style.color = 'green';
        }

        if (!/\d/.test(password.value)) {
            passwordValidationElements[1].textContent = 'Password must contain at least one number.';
            passwordValidationElements[1].classList.add('invalid');
            passwordValidationElements[1].style.color = 'red';
        } else {
            passwordValidationElements[1].textContent = 'Password contains a number.';
            passwordValidationElements[1].classList.add('valid');
            passwordValidationElements[1].style.color = 'green';
        }

        if (!/[A-Z]/.test(password.value)) {
            passwordValidationElements[2].textContent = 'Password must contain at least one uppercase character.';
            passwordValidationElements[2].classList.add('invalid');
            passwordValidationElements[2].style.color = 'red';
        } else {
            passwordValidationElements[2].textContent = 'Password contains an uppercase character.';
            passwordValidationElements[2].classList.add('valid');
            passwordValidationElements[2].style.color = 'green';
        }

        if (!/[a-z]/.test(password.value)) {
            passwordValidationElements[3].textContent = 'Password must contain at least one lowercase character.';
            passwordValidationElements[3].classList.add('invalid');
            passwordValidationElements[3].style.color = 'red';
        } else {
            passwordValidationElements[3].textContent = 'Password contains a lowercase character.';
            passwordValidationElements[3].classList.add('valid');
            passwordValidationElements[3].style.color = 'green';
        }

        if (/\s/.test(password.value)) {
            passwordValidationElements[4].textContent = 'Password must not contain spaces.';
            passwordValidationElements[4].classList.add('invalid');
            passwordValidationElements[4].style.color = 'red';
          } else {
            passwordValidationElements[4].textContent = 'Password contains no spaces.';
            passwordValidationElements[4].classList.add('valid');
            passwordValidationElements[4].style.color = 'green';
          }
      

        // Confirm password validation
        var confirmPassword = document.getElementById('conf_password');
        var confirmPasswordValidationElements = document.querySelectorAll('label[for="conf_password"] li');

        if (password.value !== confirmPassword.value) {
            confirmPasswordValidationElements[0].textContent = 'Passwords do not match.';
            confirmPasswordValidationElements[0].classList.add('invalid');
            confirmPasswordValidationElements[0].style.color = 'red';
        } else {
            confirmPasswordValidationElements[0].textContent = 'Passwords match.';
            confirmPasswordValidationElements[0].classList.add('valid');
            confirmPasswordValidationElements[0].style.color = 'green';
        }
    }
  };
  
  // Event Listeners
  document.getElementById('username_input').CustomValidation = new CustomValidation();
  document.getElementById('username_input').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });
  
  document.getElementById('first_name_input').CustomValidation = new CustomValidation();
  document.getElementById('first_name_input').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });
  
  document.getElementById('last_name_input').CustomValidation = new CustomValidation();
  document.getElementById('last_name_input').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });
  
  document.getElementById('email_input').CustomValidation = new CustomValidation();
  document.getElementById('email_input').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });

  document.getElementById('password_input').CustomValidation = new CustomValidation();
  document.getElementById('password_input').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });

  document.getElementById('conf_password').CustomValidation = new CustomValidation();
  document.getElementById('conf_password').addEventListener('keyup', function() {
    this.CustomValidation.checkInvalidity(this);
  });
  

document.getElementById("profile-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("profile-form")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch(`/auth/profile/update-profile`, {
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

    const response = await fetch(`/auth/profile/change-password`, {
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