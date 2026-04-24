const list = document.getElementById("list");
const input = document.getElementById("input");
const add_btn = document.getElementById("add_btn");


let tasks = [
    { id: 1, text: "Homework" },
    { id: 2, text: "Gym" }
];

function display() {
    list.innerHTML = "";
    tasks.forEach((task) => {
        const li = document.createElement("li");
        li.innerHTML = `
        ${task.text}
        <button onclick="deleteTask(${task.id})">❌</button>
        `;
        list.appendChild(li);
    })
}

function deleteTask(id) {
    console.log(id);
    tasks = tasks.filter(task => task.id !== id);
    display()
}

display();