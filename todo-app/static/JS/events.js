import { render_filtered_dashboard, render_dashboard} from "./render.js";
import {showMsg, check_date } from "./ui-core.js";
import {fetch_tasks, delete_account, add_task } from "./api.js";
import { getHashInfo, newHashSearch } from "./ui.js";


export async function setupSearch() {
    const search_bar = document.getElementById("search_bar");

    search_bar.addEventListener("input", () => {
       const value = search_bar.value;
       newHashSearch(value);
       
    });
}

export async function setupAddTaskForm() {
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

        const errors = [];

        if (!task_value || !end_date) {
            errors.push("Please fill in all inputs.");
        }

        if (check_date(end_date)) {
            errors.push("Please put in valid date");
        }

        if (errors.length > 0) {
            showMsg(errors, "red");
        } else {
            await add_task(task);
            task_element.value = "";
            end_date_element.value = "";
            showMsg("task added", "green");
        }
    });
}

export async function setupDeleteAccount() {
    const delete_account_btn = document.getElementById("delete_account_btn");

    delete_account_btn.addEventListener("click", async () => {
        await delete_account();
    });
}

export async function hashchange() {
    window.addEventListener("hashchange", async () => {
        let { mode, query, page, section } = getHashInfo();

        page = Number(page);
        query = query.toLowerCase();

        if (mode === "search") {
            const tasks = await fetch_tasks();

            const filtered = tasks.filter(task =>
                task.task_name.toLowerCase().includes(query)
            );

            render_filtered_dashboard(filtered, page);

        } else {
            render_dashboard(page);
        }
    });
}

