/* Add Message */
function addMessage(text, sender){

    let chatBox = document.getElementById("chat-box");

    let messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    messageDiv.classList.add(sender);

    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* Send Message */
async function sendMessage(){

    let input = document.getElementById("user-input");

    let message = input.value;

    if(message.trim() === "") return;

    addMessage(message, "user");

    input.value = "";

    try{

        let response = await fetch("/chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })
        });

        let data = await response.json();

        addMessage(data.reply, "bot");

    } catch(error){

        addMessage("Error connecting to server", "bot");
    }
}


/* Toggle Upload Menu */
function toggleMenu(){

    let menu = document.getElementById("uploadMenu");

    if(menu.style.display === "flex"){

        menu.style.display = "none";

    } else {

        menu.style.display = "flex";
    }
}


/* Variables */
let selectedFile = null;

let uploadType = "";


/* Open Popup */
function openTaskPopup(file, type){

    selectedFile = file;

    uploadType = type;

    document.getElementById("taskPopup").style.display = "flex";
}


/* Close Popup */
function closeTaskPopup(){

    document.getElementById("taskPopup").style.display = "none";

    document.getElementById("taskInput").value = "";
}


/* Upload Image */
function uploadImage(){

    let fileInput = document.getElementById("imageInput");

    let file = fileInput.files[0];

    if(!file) return;

    document.getElementById("uploadMenu").style.display = "none";

    openTaskPopup(file, "image");
}


/* Upload PDF */
function uploadPDF(){

    let fileInput = document.getElementById("pdfInput");

    let file = fileInput.files[0];

    if(!file) return;

    document.getElementById("uploadMenu").style.display = "none";

    openTaskPopup(file, "pdf");
}


/* Submit Task */
async function submitTask(){

    let task = document.getElementById("taskInput").value;

    if(task.trim() === ""){

        alert("Enter task");

        return;
    }

    let formData = new FormData();

    formData.append("file", selectedFile);

    formData.append("task", task);

    closeTaskPopup();

    try{

        let endpoint = "";

        if(uploadType === "image"){

            endpoint = "/upload-image";

            addMessage("📷 Image uploaded", "user");

        } else {

            endpoint = "/upload-pdf";

            addMessage("📄 PDF uploaded", "user");
        }

        addMessage("Task: " + task, "user");

        let response = await fetch(endpoint, {

            method:"POST",

            body:formData
        });

        let data = await response.json();

        addMessage(data.reply, "bot");

    } catch(error){

        addMessage("Upload failed", "bot");
    }
}


/* Enter Key */
document.getElementById("user-input")

.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        sendMessage();
    }
});


/* Close Menu Outside Click */
window.onclick = function(event){

    let menu = document.getElementById("uploadMenu");

    let plusBtn = document.querySelector(".plus-btn");

    if(
        !menu.contains(event.target)
        &&
        !plusBtn.contains(event.target)
    ){

        menu.style.display = "none";
    }
}