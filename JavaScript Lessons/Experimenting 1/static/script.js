const title = document.getElementById("title");
const text = document.getElementById("text");
const btn = document.getElementById("button");

btn.addEventListener("click", function() {
    if (text.textContent == "red") {
        text.textContent = "blue";
        text.style.color = "blue";
    }
    else {
        text.textContent = "red" ;
        text.style.color = "red";
    };
    
})