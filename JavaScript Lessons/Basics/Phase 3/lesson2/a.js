const btn1 = document.getElementById("btn1");
const text = document.getElementById("text");
const btn2 = document.getElementById("btn2");

const the_input = document.getElementById("the_input");
const btn3 = document.getElementById("btn3");
const magic = document.getElementById("magic");

btn1.addEventListener("click", function() {
    text.textContent = "HELLO";
})

btn2.addEventListener("click", function() {
    text.textContent = "GOODBYE";
})

btn3.addEventListener("click", function() {
    magic.textContent = the_input.value;
});
