const input = document.getElementById("taskInput");
const btn = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");

btn.addEventListener("click", () => {
    const task = input.value;
    if (task === "") return;

    const li = document.createElement("li");
    li.textContent = task + " ";

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";

    deleteBtn.addEventListener("click", () => {
        li.remove()
    })


    li.appendChild(deleteBtn)
    
    taskList.appendChild(li);
    input.value = "";
});