function CustomValidation() {
  this.invalidities = [];
}

CustomValidation.prototype = {
  getInvalidities: function() {
    return this.invalidities.join('. \n');
  },
  checkInvalidity: function(input) {
    this.invalidities = [];

    var element = document.querySelector('label[for="username_input"] li:nth-child(1)');
    if (input.value.length < 6) {
      element.textContent = 'Username must contains 6-13 characters.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.textContent = 'Username does contains 6-13 characters.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green'; 
    }

     var element = document.querySelector('label[for="username_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z0-9\s]/g)) {
      element.innerHTML = "Username does not contain letters and numbers<br>or must not contain symbols";
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.textContent = 'Username does contain letters and numbers';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    var element = document.querySelector('label[for="username_input"] li:nth-child(3)');
    if (input.value.match(/[\s]/g)) {
      element.textContent = 'Username contain spaces';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
      element.textContent = 'Username does not contain spaces';
    }


    var element = document.querySelector('label[for="first_name_input"] li:nth-child(1)');
    if (input.value.length < 2) {
      element.textContent = 'First name does not contain at least 2 characters.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.textContent = 'First name contains at least 2 characters.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green'; 
    }

    var element = document.querySelector('label[for="first_name_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z0-9\s]/g)) {
      element.textContent = 'First name must not contain symbols.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.textContent = 'First name does not contain symbols.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    var element = document.querySelector('label[for="first_name_input"] li:nth-child(3)');
    if (input.value.match(/[0-9]/g)) {
      element.textContent = 'First name must not contain numbers.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.textContent = 'First name does not contains numbers.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    var element = document.querySelector('label[for="first_name_input"] li:nth-child(4)');
    var input = document.querySelector('#first_name_input');

    var trimmedValue = input.value.trim();
    
    if (input.value !== trimmedValue) {
      element.textContent = 'First name must not have leading or trailing spaces.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'First name is valid.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    var element = document.querySelector('label[for="last_input_input"] li:nth-child(1)');
    if (input.value.length < 2) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green'; 
    }

    var element = document.querySelector('label[for="last_input_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z0-9\s]/g)) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    var element = document.querySelector('label[for="last_input_input"] li:nth-child(3)');
    if (input.value.match(/\s/g)) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    var element = document.querySelector('label[for="email_input"] li:nth-child(1)');
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var input = document.getElementById('email_input');
    if (emailPattern.test(input.value)) {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
      element.textContent = 'Contains a valid Email';
    } else {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
      element.textContent = 'Does not contain a valid Email';
    }

    var element = document.querySelector('label[for="password_input"] li:nth-child(1)');
    if (input.value.length < 8) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green'; 
    }
    
    // var element = document.querySelector('label[for="conf_password"] li:nth-child(1)');
    // if (input.value.length < 8) {
    //   element.classList.add('invalid');
    //   element.classList.remove('valid');
    //   element.style.color = 'red'; 
    // } else {
    //   element.classList.add('valid');
    //   element.classList.remove('invalid');
    //   element.style.color = 'green'; 
    // }
    var password = document.getElementById('password_input');
    var confirm_password = document.getElementById('conf_password');
    var element = document.querySelector('label[for="conf_password"] li:nth-child(1)');

    if(password.value != confirm_password.value) {
      // confirm_password.setCustomValidity("Passwords Don't Match");
      element.textContent = 'Passwords do not match';
      element.style.color = 'red';
      element.classList.add('invalid');
      element.classList.remove('valid');
    } else {
      // confirm_password.setCustomValidity('');
      element.textContent = 'Passwords match';
      element.style.color = 'green'; 
      element.classList.add('valid');
      element.classList.remove('invalid');
    }

  }
};

document.querySelector('#password_input').addEventListener('input', function() {
  var input = this;
  var feedbackElement = document.querySelector('label[for="password_input"] li:nth-child(2)');
  var uppercaseFeedback = document.querySelector('label[for="password_input"] li:nth-child(3)');
  var lowercaseFeedback = document.querySelector('label[for="password_input"] li:nth-child(4)');
  var password = input.value;
  
  if (/\d/.test(password)) {
    feedbackElement.classList.add('valid');
    feedbackElement.classList.remove('invalid');
    feedbackElement.style.color = 'green'; 
    feedbackElement.textContent = 'Password contains at least one number.';
  } else {
    feedbackElement.classList.add('invalid');
    feedbackElement.classList.remove('valid');
    feedbackElement.style.color = 'red'; 
    feedbackElement.textContent = 'Password must contain at least one number.';
  }

  if (/[A-Z]/.test(password)) {
    uppercaseFeedback.classList.add('valid');
    uppercaseFeedback.classList.remove('invalid');
    uppercaseFeedback.style.color = 'green'; 
    uppercaseFeedback.textContent = 'Password contains at least one uppercase letter.'; 
  } else {
    uppercaseFeedback.classList.add('invalid');
    uppercaseFeedback.classList.remove('valid');
    uppercaseFeedback.style.color = 'red'; 
    uppercaseFeedback.textContent = 'Password must contain at least one uppercase letter.';
  }

  if (/[a-z]/.test(password)) {
    lowercaseFeedback.classList.add('valid');
    lowercaseFeedback.classList.remove('invalid');
    lowercaseFeedback.style.color = 'green'; 
    lowercaseFeedback.textContent = 'Password contains at least one lowercase letter.'; 
  } else {
    lowercaseFeedback.classList.add('invalid');
    lowercaseFeedback.classList.remove('valid');
    lowercaseFeedback.style.color = 'red'; 
    lowercaseFeedback.textContent = 'Password must contain at least one lowercase letter.';
  }
});

// document.querySelector('#conf_password').addEventListener('input', function() {
//   var input = this;
//   var feedbackElement = document.querySelector('label[for="conf_password"] li:nth-child(2)');
//   var uppercaseFeedback = document.querySelector('label[for="conf_password"] li:nth-child(3)');
//   var lowercaseFeedback = document.querySelector('label[for="conf_password"] li:nth-child(4)');
//   var password = input.value;
  
//   if (/\d/.test(password)) {
//     feedbackElement.classList.add('valid');
//     feedbackElement.classList.remove('invalid');
//     feedbackElement.style.color = 'green'; 
//     feedbackElement.textContent = 'Password contains at least one number.';
//   } else {
//     feedbackElement.classList.add('invalid');
//     feedbackElement.classList.remove('valid');
//     feedbackElement.style.color = 'red'; 
//     feedbackElement.textContent = 'Password must contain at least one number.';
//   }

//   if (/[A-Z]/.test(password)) {
//     uppercaseFeedback.classList.add('valid');
//     uppercaseFeedback.classList.remove('invalid');
//     uppercaseFeedback.style.color = 'green'; 
//     uppercaseFeedback.textContent = 'Password contains at least one uppercase letter.'; 
//   } else {
//     uppercaseFeedback.classList.add('invalid');
//     uppercaseFeedback.classList.remove('valid');
//     uppercaseFeedback.style.color = 'red'; 
//     uppercaseFeedback.textContent = 'Password must contain at least one uppercase letter.';
//   }

//   if (/[a-z]/.test(password)) {
//     lowercaseFeedback.classList.add('valid');
//     lowercaseFeedback.classList.remove('invalid');
//     lowercaseFeedback.style.color = 'green'; 
//     lowercaseFeedback.textContent = 'Password contains at least one lowercase letter.'; 
//   } else {
//     lowercaseFeedback.classList.add('invalid');
//     lowercaseFeedback.classList.remove('valid');
//     lowercaseFeedback.style.color = 'red'; 
//     lowercaseFeedback.textContent = 'Password must contain at least one lowercase letter.';
//   }
// });

var username = document.getElementById('username_input');
username.CustomValidation = new CustomValidation();
username.addEventListener('keyup', function() {
  username.CustomValidation.checkInvalidity(this);
});

var firstname = document.getElementById('first_name_input');
firstname.CustomValidation = new CustomValidation();
firstname.addEventListener('keyup', function() {
  firstname.CustomValidation.checkInvalidity(this);
});

var lastname = document.getElementById('last_input_input');
lastname.CustomValidation = new CustomValidation();
lastname.addEventListener('keyup', function() {
  lastname.CustomValidation.checkInvalidity(this);
});

var email = document.getElementById('email_input');
email.CustomValidation = new CustomValidation();
email.addEventListener('keyup', function() {
  email.CustomValidation.checkInvalidity(this);
});

var password = document.getElementById('password_input');
password.CustomValidation = new CustomValidation();
password.addEventListener('keyup', function() {
  password.CustomValidation.checkInvalidity(this);
});

var confpass = document.getElementById('conf_password');
confpass.CustomValidation = new CustomValidation();
confpass.addEventListener('keyup', function() {
  confpass.CustomValidation.checkInvalidity(this);
});















// var password = document.getElementById("password_input")
//   , confirm_password = document.getElementById("conf_password"), element = document.querySelector('label[for="username_input"] li:nth-child(1)');


// function validatePassword(){
//   if(password.value != confirm_password.value) {
//     // confirm_password.setCustomValidity("Passwords Don't Match");
//     element.textContent('Passwords do not match');
//   } else {
//     // confirm_password.setCustomValidity('');
//     element.textContent('Passwords must match');
//   }
// }

// password.onchange = validatePassword;
// confirm_password.onkeyup = validatePassword;


document.getElementById("signup-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("signup-form")
    const formData = new FormData(form);
    
    console.log(formData)

    const response = await fetch('/auth/signup', {
        method: 'POST', 
        body: formData
    });

    console.log(response)

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        console.log(result)
    }
});

