const input = document.getElementById("input");
const btn = document.getElementById("btn");
const list = document.getElementById("list");
let tasks = []

function display() {
    list.innerHTML = "";
    tasks.forEach((task) => {
        const li = document.createElement("li");
        li.textContent = task;
        list.appendChild(li)
    });
}



btn.addEventListener("click", () => {   
    const input_value = input.value.trim()

    if (input_value.trim() === "") {
        alert("Enter a value!!!");
        return;
    }

    fetch("/add-task", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task: input_value
        })

    })

    .then(res => res.json())
    .then(data => {
        console.log(data);
    })
    

    tasks.push(input_value);
    display()
    input.value = "";
});