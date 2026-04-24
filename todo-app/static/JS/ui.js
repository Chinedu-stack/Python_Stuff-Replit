import { fetch_tasks } from "./api.js";


export function init(content) {  // this function is for when the page reloads and so that the thing you were on previously stays on when the page reloads
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"), content)
    } else {
        display("dashboard", document.getElementById("dashboard_btn"), content);
    }
}




export function display(section_name, btn, content) {   // this function hides all the pages and removes the active class from all the buttons and only shows the page that we are
    const fetched_tasks = fetch_tasks();
    const pages = document.querySelectorAll(".section"); // on and puts the active class on the btn
    pages.forEach(function(page) {
        page.style.display = "none";
    })
    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(nav_btn) {
        nav_btn.classList.remove("active")
    })

    document.getElementById(section_name).style.display = "block";
    btn.classList.add("active")
    if (section_name == "dashboard") {          // this loads the tasks onto the dashboard page
        document.getElementById(section_name).innerHTML = content[section_name];
        const ul = document.getElementById("task_list");
        fetched_tasks.forEach(function(fetched_task) {
             const li = document.createElement("li");
             li.textContent = fetched_task["task"];
             li.appendChild(ul);
        })
        window.location.hash = section_name;
        
    } else {
        document.getElementById(section_name).innerHTML = content[section_name]
        window.location.hash = section_name;
    }
    
}

