import {setupAddTaskForm, setupDeleteAccount, setupSearch, hashchange } from "./events.js";
import {render_dashboard, render_filtered_dashboard } from "./render.js";
import { fetch_tasks } from "./api.js";
import { get_filtered_tasks } from "./ui-core.js";

const page_size = 3;

export function display(section_name, btn, page_num = 1) {

    const pages = document.querySelectorAll(".section");

    pages.forEach(function(page) {
        page.classList.remove("page_active");
    });

    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(nav_btn) {
        nav_btn.classList.remove("active");
    });
    
    document.getElementById(section_name).classList.add("page_active");
    btn.classList.add("active");

    if (section_name == "dashboard") {
        update_section(section_name);
        render_dashboard(page_num)
    }   else {
        update_section(section_name);
    }
}

export function init() {
    hashchange();
    setupAddTaskForm();
    setupDeleteAccount();
    setupSearch();
    if (window.location.hash) {
        const hash = window.location.hash.slice(1);
        const params = new URLSearchParams(hash);
        const section = params.get("section");
        const page = params.get("page");
        const mode = params.get("mode");
        const query = params.get("query");
        display(section, document.getElementById(section + "_btn"), page);
    } else {
        display("dashboard", document.getElementById("dashboard_btn"));
    }
}
export  function nextPage() {
    const info = getHashInfo();
    const mode = info.mode;
    let page = Number(info.page);
    page += 1;
    update_page(page);
   
}
 
export function prevPage() {
   const info = getHashInfo();
    let page = Number(info.page);
    page -= 1;
    update_page(page);
}


export function getHashInfo() {
    const hash = window.location.hash.slice(1);
    const params = new URLSearchParams(hash);
    const section = params.get("section")
    const mode = params.get("mode");
    const query = params.get("query");
    const page = params.get("page");
    const info = {
        "mode": mode,
        "query": query,
        "page": page,
        "section": section

    }
    return info;
}

async function update_page(page) {
    const info = getHashInfo();
    const mode = info.mode;
    const query = info.query;
    const section = info.section;
    const tasks = await fetch_tasks();
    const max_pages = Math.ceil(tasks.length/3);

    if (mode == "dashboard") {
        if (page >= 1 && page <= max_pages) {
        window.location.hash = `section=${section}&page=${page}&mode=${mode}&query=${query}`;
    }  else {
        console.log("can't do that cuz it just doesn't make sense");
    }
    }   else {
            const filtered_tasks =  await get_filtered_tasks();
            const filtered_max_pages = Math.ceil(filtered_tasks.length/3)
            if (page >= 1 && page <= filtered_max_pages){
                window.location.hash = `section=${section}&page=${page}&mode=${mode}&query=${query}`;
            } else {
                console.log("can't do that cuz it just doesn't make sense");
            }

    }

    

    
}

export function newHashSearch(query) {
    const info = getHashInfo();
    const section = info.section;
    const page = 1;
    const mode = "search"
    window.location.hash = `section=${section}&page=${page}&mode=${mode}&query=${query}`;
}

function update_section(section) {
    const page = 1;
    if (section == "dashboard") {
        const mode = "dashboard";
        window.location.hash = `section=${section}&page=${page}&mode=${mode}&query=`;
    }   else {
        const mode = "add_task";
        window.location.hash = `section=${section}&page=${page}&mode=${mode}&query=`;
    }
    
}
