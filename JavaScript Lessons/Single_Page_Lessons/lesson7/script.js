const content = {
    home: "<h2>Home</h2><p>Welcome!\nI am Chinedu I will make it</p>",
    football: "<h2>Football</h2><p>I am very good at football.\nI just cooked up Swanely rangers.\nI embarrassed them!!! 🤣🤣🤣</p>",
    coding: "<h2>Coding</h2><p>Right now I'm learning coding.\nIt is just about staying consistent for a long time and i will succeed</p>",
    school: "<h2>School</h2><p>It's okay.\nI walk in. I do work don't talk too much and walk right back out</p>"

}

function init() {
    document.getElementById("home").style.display = 'block';
    document.getElementById("home").innerHTML = content['home'];
    document.getElementById("nav-btn-home").classList.add('active');
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
}

init()