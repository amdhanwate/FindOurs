function registrationSuccess(){
    document.location.href = "/findours/web/home.html";
    alert("Registration Successful!");
}

function logout(){
    document.location.href = "login.html";
}

function scanAnimation(){
    "use strict";
    document.getElementById('diode').classList.add('diode');
    document.getElementById('laser').classList.add('laser');

    setTimeout(() => {
        document.getElementById('diode').classList.remove('diode');
    document.getElementById('laser').classList.remove('laser');
    }, 2000);
}