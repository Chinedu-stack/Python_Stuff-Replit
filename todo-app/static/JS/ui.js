import { fetch_tasks, edit_task, add_task, delete_task, task_done} from "./api.js";

export function init() {
    setupAddTaskForm();
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"));
    } else {
        display("dashboard", document.getElementById("dashboard_btn"));
    }
}

function showMsg(message, color) {
    const msg = document.getElementById("message");
    msg.textContent = message;
    msg.style.color = color;

    setTimeout(() => {
        msg.textContent = "";
    }, 3000);
}

export  function display(section_name, btn) {
    window.location.hash = section_name;
    const pages = document.querySelectorAll(".section");

    pages.forEach(function(page) {
        page.style.display = "none";
    });

    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(nav_btn) {
        nav_btn.classList.remove("active");
    });

    document.getElementById(section_name).style.display = "block";
    btn.classList.add("active");

    if (section_name == "dashboard") {
        render_dashboard()
    }
}

async function setupAddTaskForm() {
    const submit_btn = document.getElementById("submit_btn");

    submit_btn.addEventListener("click", async () => {

    const task_value = document.getElementById("name").value.trim();
    const start_date = document.getElementById("start-date").value.trim();
    const end_date = document.getElementById("end-date").value.trim();

    const task_element = document.getElementById("name");
    const start_date_element = document.getElementById("start-date");
    const end_date_element = document.getElementById("end-date");



    const task = {
        task: task_value,
        start_date: start_date,
        end_date: end_date

    };


    if (!task_value || !start_date || !end_date) {
        const error = "Please fill in all inputs.";
        showMsg(error, "red");
    } else {
        await add_task(task); 
        task_element.value = "";
        start_date_element.value = "";
        end_date_element.value = "";
        showMsg("task added", "green");

    }
    })
    
}

async function render_dashboard() {
    const tasks = await fetch_tasks();

    const ul = document.getElementById("task_list");
    ul.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");
        li.textContent = task.task;

        if (task.completed) {
            li.classList.add("done");
            li.innerHTML = `${task.task}✔️`;
        } else {
            li.textContent = task.task;
            li.classList.add("not_done")
        }

        const delete_btn = document.createElement("button");
        delete_btn.textContent = "Delete";

        
        delete_btn.addEventListener("click", async () => {
            await delete_task(task.task);
            render_dashboard(); // refresh list
        });

        const done_btn = document.createElement("button");
        done_btn.textContent = "done"

        done_btn.addEventListener("click", async () => {
            await task_done(task.task);
            render_dashboard();
        })

        const edit_btn = document.createElement("button");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", async () => {
            const input = document.createElement("input");
            input.value = task.task;

            const save_btn = document.createElement("button");
            save_btn.textContent = "Save";

            li.appendChild(input);
            li.appendChild(save_btn);

            save_btn.addEventListener("click", async () => {
                await edit_task(task.task, input.value);

                input.remove();
                save_btn.remove();

                render_dashboard();
            });
        });

        li.appendChild(done_btn);
        li.appendChild(edit_btn);
        li.appendChild(delete_btn);
        ul.appendChild(li);
    });
 }

 