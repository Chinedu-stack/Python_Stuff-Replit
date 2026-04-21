let content = {};


async function loadContent() {
    const response = await fetch('content.json');
    content = await response.json();
    init()
}







function init() {
    if (window.location.hash) {
        const section = window.location.hash.slice(1);
        display(section, document.getElementById("nav-btn-" + section))
    } else {
        display("home", document.getElementById('nav-btn-home'));
    }
}


function display(page_id, btn) {
    const pages = document.querySelectorAll(".section");
    pages.forEach(function(page) {
        page.style.display = "none";
    })

    const nav_btns = document.querySelectorAll("nav button");
    nav_btns.forEach(function(btn) {
        btn.classList.remove("active")
    })

    document.getElementById(page_id).style.display = "block";
    document.getElementById(page_id).innerHTML = content[page_id]
    btn.classList.add("active");
    window.location.hash = page_id;
}

loadContent()