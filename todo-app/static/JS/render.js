import {fetch_tasks, delete_task, task_done, edit_task} from "./api.js";
import {nextPage, prevPage } from "./ui.js";


export async function render_dashboard(current_page) {
    const tasks = await fetch_tasks();
    const page_size = 3;
    const ol = document.getElementById("task_list");
    ol.innerHTML = "";
    const mode = "dashboard";


    let start = (current_page - 1) * page_size;
    let end = start + page_size;

    let paginatedTasks = tasks.slice(start, end);


    paginatedTasks.forEach(task => {

        const li = document.createElement("li");

        const task_text = document.createElement("span");

        if (task.completed) {
            task_text.classList.add("done");
            task_text.textContent = `${task.task_name}✔️`;
        } else {
            task_text.classList.add("not_done");
            task_text.textContent = task.task_name;
        }

        li.appendChild(task_text);

        const delete_btn = document.createElement("button");
        delete_btn.classList.add("crud_btns");
        delete_btn.textContent = "Delete";

        delete_btn.addEventListener("click", async () => {
            await delete_task(task.task_name);
            render_dashboard();
        });

        const done_btn = document.createElement("button");
        done_btn.classList.add("crud_btns");
        done_btn.textContent = "done";

        done_btn.addEventListener("click", async () => {
            await task_done(task.task_name);
            render_dashboard();
        });

        const edit_btn = document.createElement("button");
        edit_btn.classList.add("crud_btns");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", async () => {

            const input = document.createElement("input");
            input.classList.add("edit_input");
            input.value = task.task_name;

            const save_btn = document.createElement("button");
            save_btn.classList.add("crud_btns");
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

        ol.appendChild(li);
    });

    if (tasks.length > page_size) {

    const next_page = document.createElement("button");
    next_page.textContent = "Next Page";
    next_page.classList.add("create_task_btn");

    next_page.addEventListener("click", async () => {
        nextPage(mode);
    });

    const prev_page = document.createElement("button");
    prev_page.textContent = "Previous Page";
    prev_page.classList.add("create_task_btn");

    prev_page.addEventListener("click", () => {
        prevPage(mode);
    });

    ol.appendChild(prev_page);
    ol.appendChild(next_page);
}
}

export async function render_filtered_dashboard(filtered_tasks, current_page=1) {
    const ol = document.getElementById("task_list");
    ol.innerHTML = "";
    const page_size = 3;
    const state = "search";


    let start = (current_page - 1) * page_size;
    let end = start + page_size;

    

    if (filtered_tasks.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No Results";
        li.classList.add("not_done");
        ol.appendChild(li);
    }

    let paginatedTasks = filtered_tasks.slice(start, end);

    paginatedTasks.forEach(task => {

        const li = document.createElement("li");
        li.textContent = task.task_name;

        if (task.completed) {
            li.classList.add("done");
            li.innerHTML = `${task.task_name}✔️`;
        } else {
            li.textContent = task.task_name;
            li.classList.add("not_done");
        }

        const delete_btn = document.createElement("button");
        delete_btn.classList.add("crud_btns");
        delete_btn.textContent = "Delete";

        delete_btn.addEventListener("click", async () => {
            await delete_task(task.task_name);
            const tasks = await fetch_tasks();
            const value = search_bar.value.toLowerCase();
            const filtered = tasks.filter(task =>
                task.task_name.toLowerCase().includes(value)
            );
            render_filtered_dashboard(filtered);
        });

        const done_btn = document.createElement("button");
        done_btn.classList.add("crud_btns");
        done_btn.textContent = "done";

        done_btn.addEventListener("click", async () => {
            await task_done(task.task_name);
            const tasks = await fetch_tasks();
            const value = search_bar.value.toLowerCase();
            const filtered = tasks.filter(task =>
                task.task_name.toLowerCase().includes(value)
            );
            render_filtered_dashboard(filtered);
        });

        const edit_btn = document.createElement("button");
        edit_btn.classList.add("crud_btns");
        edit_btn.textContent = "Edit";

        edit_btn.addEventListener("click", async () => {
            const input = document.createElement("input");
            input.value = task.task_name;

            const save_btn = document.createElement("button");
            save_btn.classList.add("crud_btns");
            save_btn.textContent = "Save";

            li.appendChild(input);
            li.appendChild(save_btn);

            save_btn.addEventListener("click", async () => {
                await edit_task(task.task_name, input.value);

                input.remove();
                save_btn.remove();

                const tasks = await fetch_tasks();
                const value = search_bar.value.toLowerCase();
                const filtered = tasks.filter(task =>
                    task.task_name.toLowerCase().includes(value)
                );

                render_filtered_dashboard(filtered);
            });
        });

        li.appendChild(done_btn);
        li.appendChild(edit_btn);
        li.appendChild(delete_btn);
        ol.appendChild(li);
    });

    if (filtered_tasks.length > page_size) {

    const next_page = document.createElement("button");
    next_page.textContent = "Next Page";
    next_page.classList.add("create_task_btn");

    next_page.addEventListener("click", async () => {
        nextPage(state, filtered_tasks, current_page);
    });

    const prev_page = document.createElement("button");
    prev_page.textContent = "Previous Page";
    prev_page.classList.add("create_task_btn");

    prev_page.addEventListener("click", () => {
        prevPage(state, filtered_tasks, current_page);
    });

    ol.appendChild(prev_page);
    ol.appendChild(next_page);
}
    
}

