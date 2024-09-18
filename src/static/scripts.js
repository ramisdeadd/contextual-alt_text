document.getElementById("upload-article").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = document.getElementById("upload-article")
    const formData = new FormData(form);

    console.log(formData)

    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    } 

    const result = await response.json();
    
    document.getElementById("getalttext").value = result['generated-alt-text'];
    document.getElementById("getcaption").value = result['generated-image-caption'];
});


var loadFile = function(event) {
    var output = document.getElementById('output');
    const border = document.querySelector('.uploadimage');
    const border2 = document.getElementById('imagebox')
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) 
    }

    border.style.border = "unset";
};  