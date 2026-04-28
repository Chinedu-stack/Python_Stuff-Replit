import { fetch_tasks } from "./api.js";
import { add_task } from "./api.js";

export function init() {
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

export async function display(section_name, btn) {
    const fetched_tasks = await fetch_tasks();
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
        const ul = document.getElementById("task_list");
        ul.innerHTML = "";

        fetched_tasks.forEach(function(fetched_task) {
            const li = document.createElement("li");
            li.textContent = fetched_task["task"];
            ul.appendChild(li);
        });

        window.location.hash = section_name;

    } else if (section_name == "add_task") {
        const submit_btn = document.getElementById("submit_btn");

        submit_btn.addEventListener("click", function() {

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
                add_task(task); 
                task_element.textContent = "";
                start_date_element.textContent = "";
                end_date_element.textContent = "";
                showMsg("task added", "green");

            }
        window.location.hash = section_name;
        });

        
    } else {
        window.location.hash = section_name;
    }
    
}