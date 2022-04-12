function darkMode(){
    if (document.getElementById("header").className == "header_light"){
        document.getElementById("header").className = "header_dark";
        document.getElementById("footer").className = "footer_dark";
        document.getElementById("body").className = "body_dark";
    }
    else{
        document.getElementById("header").className = "header_light";
        document.getElementById("footer").className = "footer_light";
        document.getElementById("body").className = "body_light";
    }
    
}
