import {setupAddTaskForm, setupDeleteAccount, setupSearch, hashchange } from "./events.js";
import {render_dashboard } from "./render.js";
import { fetch_tasks } from "./api.js";

let current_page = 1;
const page_size = 3;

export function display(section_name, btn) {
    if (section_name == "dashboard") {
        window.location.hash = `section=${section_name}&page=1`
    }
    window.location.hash = section_name;
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
        render_dashboard(current_page)
    }
}

export function init() {
    hashchange();
    setupAddTaskForm();
    setupDeleteAccount();
    setupSearch();
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"));
    } else {
        display("dashboard", document.getElementById("dashboard_btn"));
    }
}
export async function nextPage() {
    const tasks = await fetch_tasks();
    const totalPages = Math.ceil(tasks.length/page_size);
    if (current_page < totalPages ) {
        current_page += 1;
        updateHash(current_page);
    }
    
}

export function prevPage() {
    if (current_page > 1) {
        current_page -= 1;
        updateHash(current_page);
    }
}


export function getPageFromHash() {
    const hash = window.location.hash;

    if (hash.includes("page=")) {
        const page = parseInt(hash.split("page=")[1]);
        return isNaN(page) ? 1 : page;
    }

    return 1;
}

function updateHash(page) {
    window.location.hash = `section=dashboard&page=${page}`;
}


