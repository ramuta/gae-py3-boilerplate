let useSendGridButton = document.getElementById("dropdownMenuSendGrid");
let sendGridDiv = document.getElementById("sendGridDiv");
let authOptionsDiv = document.getElementById("authOptionsDiv");

function useSendGrid(choice) {
    useSendGridButton.textContent = "Use SendGrid emailing: " + choice;

    if (choice == "NO") {
        sendGridDiv.style.display = "none";
        authOptionsDiv.style.display = "none";
    } else {
        sendGridDiv.style.display = "block";
        authOptionsDiv.style.display = "block";
    }
}
