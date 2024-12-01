const alt_text_output = document.getElementById("getalttext");
const image_caption_output = document.getElementById("getcaption");
const save_alt_button = document.getElementById("save-alt");
const save_cap_button = document.getElementById("save-caption");
const file_upload_input = document.getElementById("getimage");
const context_input = document.getElementById('gettext');
const generate_btn = document.getElementById('generate_btn');
const select_nlp = document.getElementById('nlp');
const select_cv = document.getElementById('cv');
const upload_btn = document.getElementById("upload-article")

function isFile() {
    return file_upload_input.files.length !== 0;
}

function isContext() {
    return context_input.value.trim() !== '';
}

function validGeneration() {
    if (isContext() && isFile()) {
        generate_btn.disabled = false
    } else {
        generate_btn.disabled = true
    }   
}

function enableEditing() {
    if (alt_text_output.textContent == '' && image_caption_output.value == '') {
        alt_text_output.contentEditable = false
        image_caption_output.disabled = true

        save_alt_button.disabled = true
        save_cap_button.disabled = true
    } else {
        alt_text_output.contentEditable = true
        image_caption_output.disabled = false

        save_alt_button.disabled = false
        save_cap_button.disabled = false
    }
}

function resetOutputs() {
    alt_text_output.textContent = ''
    image_caption_output.value = ''
}

function enableGenerate() {
    /* Generate Inputs Enabled */
    context_input.disabled = false
    file_upload_input.disabled = false
}

function disableGenerate() {
    /* Generate Inputs Disabled */
    context_input.disabled = true
    generate_btn.disabled = true
    file_upload_input.disabled = true
}

async function generateAlt() {
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    disableGenerate()

    const response = await fetch('/post/', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        alt_text_output.textContent = result['generated-alt-text'];
        image_caption_output.textContent = result['generated-image-caption'];
    }

    enableGenerate()
    enableEditing()
}

upload_btn.addEventListener("submit", async (e) => {
    e.preventDefault();

    let file_uploaded = isFile()
    let text_uploaded = isContext()

    if (file_uploaded == false || text_uploaded == false) {
        console.log("Image File or Article Content is Missing")
        return 
    } 

    generateAlt()
});

/* Extra Validation for File & Context */

context_input.addEventListener("input", async (e) => {
    resetOutputs() 
    validGeneration()
    enableEditing()
})

/* File Upload Functionality */

file_upload_input.addEventListener("change", async (e) => {
    let output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox');

    output.src = URL.createObjectURL(e.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src);
    };

    border.style.border = "unset";
    resetOutputs() 
    validGeneration()
    enableEditing()
});

select_cv.addEventListener("change", async (e) => {
    resetOutputs() 
    validGeneration()
    enableEditing()
});

select_nlp.addEventListener("change", async (e) => {
    resetOutputs() 
    validGeneration()
    enableEditing()
});

/* Save Output Functionalities */

save_alt_button.addEventListener("click", async (e) => {
    
    let alt_text_content = alt_text_output.textContent

    const response = await fetch('/post/save-alt-text/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({alt_text: alt_text_content})
    });

    if (response.status == 401 ) {
        window.location.href = '/auth/login';
    } 

    if (response.ok) {
        console.log("Alt-Text Saved Successfully")
    } else {
        console.log("Saving Error")
    }
})

save_cap_button.addEventListener("click", async (e) => {
    
    let image_caption_content = image_caption_output.textContent

    console.log(`IMAGE CAPTION` + image_caption_content)

    const response = await fetch('/post/save-image-caption/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({image_caption: image_caption_content})
    });

    if (response.status == 401 ) {
        window.location.href = '/auth/login';
    } 

    if (response.ok) {
        console.log("Image Caption Saved Successfully")
    } else {
        console.log("Saving Error")
    }
})

/* Copy Output Functionalities */

document.getElementById("copy-alt").addEventListener("click", async (e) => {

    navigator.clipboard.writeText(alt_text_output.textContent);
    console.log("Alt-Text Copied to Clipboard")

    alt_text_output.blur();
});

document.getElementById("copy-caption").addEventListener("click", async (e) => {
    e.preventDefault()
    image_caption_output.select();
    image_caption_output.setSelectionRange(0, 9999);

    navigator.clipboard.writeText(image_caption_output.value);
    console.log("Image Caption Copied to Clipboard")

    image_caption_output.blur();
});

document.getElementById('getimage').addEventListener('change', function () {
    if (this.files && this.files.length > 0) {
        document.querySelector('.replacer-button').style.display = 'none';

        const output = document.getElementById('output');
        const file = this.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            output.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
});

