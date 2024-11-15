const alt_text_output = document.getElementById("getalttext");
const image_caption_output = document.getElementById("getcaption");
const save_alt_button = document.getElementById("save-alt");
const save_cap_button = document.getElementById("save-caption");
const file_upload_input = document.getElementById("getimage");
const context_input = document.getElementById('gettext');
const generate_btn = document.getElementById('generate_btn');

function isFile() {
    return file_upload_input.files.length !== 0;
}

function isContext() {
    return context_input.value.trim() !== '';
}

function enableGenerate() {

    /* Generate Inputs Enabled */
    context_input.disabled = false
    generate_btn.disabled = false

    context_input.value = ''
    alt_text_output.value = ''
    image_caption_output.value = ''

    /* Save Functions Disabled */
    save_alt_button.disabled = true
    save_cap_button.disabled = true

}

function disableGenerate() {

    /* Generate Inputs Disabled */
    context_input.disabled = true
    generate_btn.disabled = true

    /* Save Functions Enabled */
    save_alt_button.disabled = false
    save_cap_button.disabled = false
}

async function generateAlt() {
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    const response = await fetch('/post/', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        alt_text_output.value = result['generated-alt-text'];
        image_caption_output.value = result['generated-image-caption'];
    }

    disableGenerate()
}

document.getElementById("upload-article").addEventListener("submit", async (e) => {
    e.preventDefault();

    let file_uploaded = isFile()
    let text_uploaded = isContext()

    if (file_uploaded == false || text_uploaded == false) {
        console.log("Image File or Article Content is Missing")
        return 
    } 

    generateAlt()
});

save_alt_button.addEventListener("click", async (e) => {
    e.preventDefault()
    
    let alt_text_content = alt_text_output.value

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


const loadFile = function(event) {
    let output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox')

    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) 
    }

    border.style.border = "unset";
    enableGenerate()
};  

document.getElementById("copy-alt").addEventListener("click", async (e) => {
    e.preventDefault()
    alt_text_output.select();
    alt_text_output.setSelectionRange(0, 9999);

    navigator.clipboard.writeText(alt_text_output.value);
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

