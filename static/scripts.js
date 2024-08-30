const text_input = document.getElementById("gettext");
const sumbit_btn = document.getElementById("generate");

/* var uploaded_image = "";

image_input.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploaded_image = reader.result;
        document.querySelector("#display_image").style.backgroundImage = 'url(${uploaded_image})';
    });
    reader.readAsDataURL(this.files[0]);
})

 */

// Josh - Generation Test
document.getElementById("upload-article").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    console.log(response)

    const result = await response.json()
    console.log(result)
});

