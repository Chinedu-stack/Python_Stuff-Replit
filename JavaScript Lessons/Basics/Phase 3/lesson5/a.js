const input = document.getElementById("input");
const btn = document.getElementById("btn");
const ol = document.getElementById("task_list");

let tasks = [];

function display() {
    ol.innerHTML = "";

    tasks.forEach((task, index) => {
        const li = document.createElement("li");
        li.textContent = task;

        // DELETE BUTTON
        const delete_btn = document.createElement("button");
        delete_btn.textContent = "Delete";

        delete_btn.addEventListener("click", () => {
            tasks.splice(index, 1);
            display();
        });

        li.appendChild(delete_btn);

        // EDIT BUTTON
        const edit_btn = document.createElement("button");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", () => {
            const edit_input = document.createElement("input");
            const submit = document.createElement("button");

            submit.textContent = "Submit";

            li.appendChild(edit_input);
            li.appendChild(submit);

            submit.addEventListener("click", () => {
                const new_value = edit_input.value;

                if (new_value.trim() === "") {
                    alert("Enter a value!!!");
                    return;
                }

                tasks[index] = new_value.trim();
                display();
            });
        });

        li.appendChild(edit_btn);
        ol.appendChild(li);
    });
}

btn.addEventListener("click", function () {
    const task_value = input.value.trim();

    if (task_value === "") {
        alert("enter a value");
        return;
    }

    tasks.push(task_value);
    display();
    input.value = ""
});