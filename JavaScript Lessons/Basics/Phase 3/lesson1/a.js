let title = document.getElementById("title");
let info = document.querySelector(".info");
let info2 = document.querySelector(".info2");
let addTaskBtn = document.getElementById("addTaskBtn");

addTaskBtn.addEventListener("click", function() {
    info.textContent = " Task 1. Get Better";
    title.textContent = "My Tasks";
    info2.textContent = "Your task is due Next week tuesday.";
});

