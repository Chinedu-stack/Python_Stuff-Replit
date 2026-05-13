import { fetch_tasks, edit_task, add_task, delete_task, task_done, delete_account} from "./api.js";

export function init() {
    setupAddTaskForm();
    setupDeleteAccount();
    search();
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"));
    } else {
        display("dashboard", document.getElementById("dashboard_btn"));
    }
}

function showMsg(message, color) {
    const msg_list = document.getElementById("msg_list");


    msg_list.style.color = color;
    msg_list.textContent = "";

    if (Array.isArray(message)) {
        message.forEach(function(msg_element) {
            const li = document.createElement("li");
            li.textContent = msg_element;
            msg_list.appendChild(li);
        })
    }   else {
        const li = document.createElement("li");
        li.textContent = message;
        msg_list.appendChild(li);
    }



    setTimeout(() => {
        msg_list.textContent = "";
    }, 1000);
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
    const end_date = document.getElementById("end-date").value.trim();

    const task_element = document.getElementById("name");
    const end_date_element = document.getElementById("end-date");



    const task = {
        task: task_value,
        end_date: end_date

    };

    const errors = []


    if (!task_value || !end_date) {
        const error = "Please fill in all inputs.";
        errors.push(error)
    }
    if (check_date(end_date)) {
        const error = "Please put in valid date"
        errors.push(error)
    }   

    if (errors.length > 0) {
        showMsg(errors, "red")
    } else {
        await add_task(task); 
        task_element.value = "";
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
        li.textContent = task.task_name;

        if (task.completed) {
            li.classList.add("done");
            li.innerHTML = `${task.task_name}✔️`;
        } else {
            li.textContent = task.task_name;
            li.classList.add("not_done")
        }

        const delete_btn = document.createElement("button");
        delete_btn.textContent = "Delete";

        
        delete_btn.addEventListener("click", async () => {
            await delete_task(task.task_name);
            render_dashboard(); // refresh list
        });

        const done_btn = document.createElement("button");
        done_btn.textContent = "done"

        done_btn.addEventListener("click", async () => {
            await task_done(task.task_name);
            render_dashboard();
        })

        const edit_btn = document.createElement("button");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", async () => {
            const input = document.createElement("input");
            input.value = task.task_name;

            const save_btn = document.createElement("button");
            save_btn.textContent = "Save";

            li.appendChild(input);
            li.appendChild(save_btn);

            save_btn.addEventListener("click", async () => {
                await edit_task(task.task_name, input.value);

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

 async function setupDeleteAccount() {
    const delete_account_btn = document.getElementById("delete_account_btn")
    delete_account_btn.addEventListener("click", async ()=> {
        await delete_account();
    })
 }

 function check_date(end_date) {
    const today = new Date()
    today.setHours(0,0,0,0)
    
    const date = new Date(end_date)
    if (date < today) {
        return true
    } else {
        return false
    }
 }

 async function search() {
    const tasks = await fetch_tasks();
    const search_bar = document.getElementById("search_bar");
    search_bar.addEventListener("input", () => {
        const value = search_bar.value.toLowerCase();

        const filtered = tasks.filter(task => 
            task.task_name.toLowerCase().includes(value)
        );

        render_filtered_dashboard(filtered)
    })
 }

 async function render_filtered_dashboard(filtered_tasks) {
    const ul = document.getElementById("task_list");
    ul.innerHTML = "";

    filtered_tasks.forEach(task => {

        const li = document.createElement("li");
        li.textContent = task.task_name;

        if (task.completed) {
            li.classList.add("done");
            li.innerHTML = `${task.task_name}✔️`;
        } else {
            li.textContent = task.task_name;
            li.classList.add("not_done")
        }

        const delete_btn = document.createElement("button");
        delete_btn.textContent = "Delete";

        
        delete_btn.addEventListener("click", async () => {
            await delete_task(task.task_name);
            render_filtered_dashboard(filtered_tasks); // refresh list
        });

        const done_btn = document.createElement("button");
        done_btn.textContent = "done"

        done_btn.addEventListener("click", async () => {
            await task_done(task.task_name);
            render_filtered_dashboard(filtered_tasks);
        })

        const edit_btn = document.createElement("button");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", async () => {
            const input = document.createElement("input");
            input.value = task.task_name;

            const save_btn = document.createElement("button");
            save_btn.textContent = "Save";

            li.appendChild(input);
            li.appendChild(save_btn);

            save_btn.addEventListener("click", async () => {
                await edit_task(task.task_name, input.value);

                input.remove();
                save_btn.remove();

                render_filtered_dashboard(filtered_tasks);
            });
        });

        li.appendChild(done_btn);
        li.appendChild(edit_btn);
        li.appendChild(delete_btn);
        ul.appendChild(li);
    });
 }
 