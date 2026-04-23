export function init(content) {
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById(section + "_btn"), content)
    } else {
        display("dashboard", document.getElementById("dashboard_btn"), content);
    }
}




export function display(section_name, btn, content) {
    const pages = document.querySelectorAll(".section");
    pages.forEach(function(page) {
        page.style.display = "none";
    })
    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(nav_btn) {
        nav_btn.classList.remove("active")
    })

    document.getElementById(section_name).style.display = "block";
    btn.classList.add("active")
    document.getElementById(section_name).innerHTML = content[section_name]
    window.location.hash = section_name;
}

