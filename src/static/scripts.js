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

    document.getElementById("getresult").innerText = result['Generated Alt-Text'];
});


var loadFile = function(event) {
    var output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox')
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }

    border.style.border = "unset";
};  