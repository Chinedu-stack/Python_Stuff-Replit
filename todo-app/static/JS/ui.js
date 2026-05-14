import {setupAddTaskForm, setupDeleteAccount, setupSearch } from "./events.js";
import {render_dashboard } from "./render.js";

export function display(section_name, btn) {
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

export function init() {
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






