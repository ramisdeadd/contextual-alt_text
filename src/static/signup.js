function CustomValidation() {
  this.invalidities = [];
}

CustomValidation.prototype = {
  getInvalidities: function() {
    return this.invalidities.join('. \n');
  },

  checkInvalidity: function(input) {
    this.invalidities = [];

    if (input.id === 'username_input') {
      this.validateUsername(input);
    } else if (input.id === 'first_name_input') {
      this.validateFirstName(input);
    } else if (input.id === 'last_input_input') {
      this.validateLastName(input);
    } else if (input.id === 'email_input') {
      this.validateEmail(input);
    } else if (input.id === 'conf_password' || input.id === 'password_input') {
      this.validateConfirmPassword();
    }
  },

  validateUsername: function(input) {
    let element = document.querySelector('label[for="username_input"] li:nth-child(1)');
    if (input.value.length < 6 || input.value.length > 13) {
      element.textContent = 'Username must contain 6-13 characters.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'Username contains 6-13 characters.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="username_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z0-9\s]/g)) {
      element.innerHTML = "Username should not contain symbols.";
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'Username does not contain symbols.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="username_input"] li:nth-child(3)');
    if (input.value.match(/[\s]/g)) {
      element.textContent = 'Username should not contain spaces.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'Username does not contain spaces.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }
  },

  validateFirstName: function(input) {
    let element = document.querySelector('label[for="first_name_input"] li:nth-child(1)');
    if (input.value.length < 2) {
      element.textContent = 'First name must contain at least 2 characters.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'First name contains at least 2 characters.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="first_name_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z\s]/g)) {
      element.textContent = 'First name should not contain symbols.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'First name does not contain symbols.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="first_name_input"] li:nth-child(3)');
    if (input.value.match(/[0-9]/g)) {
      element.textContent = 'First name should not contain numbers.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'First name does not contain numbers.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="first_name_input"] li:nth-child(4)');
    let trimmedValue = input.value.trim();
    if (input.value !== trimmedValue) {
      element.textContent = 'First name should not have leading or trailing spaces.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'First name has no leading or trailing spaces.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }
  },

  validateLastName: function(input) {
    let element = document.querySelector('label[for="last_input_input"] li:nth-child(1)');
    if (input.value.length < 2) {
      element.textContent = 'Last name must contain at least 2 characters.';
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red';
    } else {
      element.textContent = 'Last name contains at least 2 characters.';
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';
    }

    element = document.querySelector('label[for="last_input_input"] li:nth-child(2)');
    if (input.value.match(/[^a-zA-Z0-9\s]/g)) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

    element = document.querySelector('label[for="last_input_input"] li:nth-child(3)');
    if (input.value.match(/\s/)) {
      element.classList.add('invalid');
      element.classList.remove('valid');
      element.style.color = 'red'; 
    } else {
      element.classList.add('valid');
      element.classList.remove('invalid');
      element.style.color = 'green';  
    }

  },

  validateEmail: function(input) {
    let element = document.querySelector('label[for="email_input"] li:nth-child(1)');
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
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

    
  },

  validateConfirmPassword: function() {
      let password = document.getElementById('password_input');
      let confirmPassword = document.getElementById('conf_password');
      let element = document.querySelector('label[for="conf_password"] li:nth-child(1)');
  
      if (password.value !== confirmPassword.value) {
        element.textContent = 'Passwords do not match';
        element.style.color = 'red';
        element.classList.add('invalid');
        element.classList.remove('valid');
      } else {
        element.textContent = 'Passwords match';
        element.style.color = 'green';
        element.classList.add('valid');
        element.classList.remove('invalid');
      }
  }
};

// Attach validation to each input independently
['username_input', 'first_name_input', 'last_input_input', 'email_input', 'password_input', 'conf_password'].forEach(function(inputId) {
  let inputElement = document.getElementById(inputId);
  inputElement.CustomValidation = new CustomValidation();
  inputElement.addEventListener('keyup', function() {
    inputElement.CustomValidation.checkInvalidity(this);
  });
});


document.querySelector('#password_input').addEventListener('input', function() {
  var input = this;
  var numFeedback = document.querySelector('label[for="password_input"] li:nth-child(1)');
  var feedbackElement = document.querySelector('label[for="password_input"] li:nth-child(2)');
  var uppercaseFeedback = document.querySelector('label[for="password_input"] li:nth-child(3)');
  var lowercaseFeedback = document.querySelector('label[for="password_input"] li:nth-child(4)');
  var password = input.value;
  

  if (input.value.length < 8) {
    numFeedback.classList.add('invalid');
    numFeedback.classList.remove('valid');
    numFeedback.style.color = 'red'; 
  } else {
    numFeedback.classList.add('vnumFeedbackalid');
    numFeedback.classList.remove('invalid');
    numFeedback.style.color = 'green'; 
  }

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

