import {setupAddTaskForm, setupDeleteAccount, setupSearch, hashchange } from "./events.js";
import {render_dashboard } from "./render.js";
import { fetch_tasks } from "./api.js";

const page_size = 3;

export function display(section_name, btn, page_num = 1) {

    const current_page = page_num;

    if (section_name == "dashboard") {
        window.location.hash = `section=${section_name}&page=${current_page}`
    } else {
        window.location.hash = `section=${section_name}`;
    }
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
        const hash = window.location.hash.slice(1);
        const params = new URLSearchParams(hash);
        const section = params.get("section")
        const page = params.get("page");
        display(section, document.getElementById(section + "_btn"), page);
    } else {
        display("dashboard", document.getElementById("dashboard_btn"));
    }
}
export async function nextPage() {
    const tasks = await fetch_tasks();
    const totalPages = Math.ceil(tasks.length/page_size);
    let current_page = getPageFromHash();
    if (current_page < totalPages ) {
        current_page += 1;
        updateHash(current_page);
        console.log("Next page: ");
    }
    
}

export function prevPage() {
    let current_page = getPageFromHash();
    if (current_page > 1) {
        current_page -= 1;
        updateHash(current_page);
        console.log("Previous page: ");
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


