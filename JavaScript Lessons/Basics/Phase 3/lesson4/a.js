const input = document.getElementById("taskInput");
const btn = document.getElementById("addBtn");
const list = document.getElementById("taskList");

btn.addEventListener("click", function() {
    const value = input.value.trim();

    if (value === "") {
        return;
    }

    const li = document.createElement("li");
    li.textContent = value + " "
    const deleteBtn = document.createElement("button");

    deleteBtn.textContent = "Delete";
    deleteBtn.addEventListener("click", function() {
        li.remove()
    });

    li.appendChild(deleteBtn);
    list.appendChild(li);

    input.value = "";


})