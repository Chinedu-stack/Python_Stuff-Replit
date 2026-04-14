const input = document.getElementById("input");
const btn = document.getElementById("btn");
const ol = document.getElementById("task_list");
const color_btn = document.getElementById("color_btn");

function color() {
    let colors = ["red", "yellow", "green", "orange", "indigo"];
    let num = Math.floor(Math.random() * colors.length)
    return colors[num]
    
}


btn.addEventListener("click", function() {
    const task_value = input.value.trim();

      if (task_value === "") {
        return;
    }
    const li = document.createElement("li");
    li.textContent = task_value;

    const delete_btn = document.createElement("button");
    delete_btn.textContent = "Delete";
    delete_btn.addEventListener("click", function () {
        li.remove()
    });
       
    li.appendChild(delete_btn);
    ol.appendChild(li);

    input.value = "";
});

color_btn.addEventListener("click", function() {
    ol.style.color = color()
});
