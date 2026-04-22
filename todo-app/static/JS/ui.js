export function init() {
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"))
    } else {
        display("home", document.getElementById("dashboard_btn"));
    }
}




export function display(section, btn) {
    const pages = document.querySelectorAll(".section");
    pages.forEach(function(page) {
        page.style.display = "none";
    })
    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(nav_btn) {
        nav_btn.classList.remove("active")
    })

    document.getElementById(section).style.display = "block";
    btn.classList.add("active")
    document.getElementById(section).innerHTML = content[section]
    window.location.hash = section;
}

