import { display } from "./ui.js";
import { init } from "./ui.js";


document.addEventListener("DOMContentLoaded", async () => {

    document.querySelectorAll("nav button").forEach(btn => {  // this runs the display function each time one of the nav buttons is being clicked 
        btn.addEventListener("click", () => {                 // it gets the section name, the btn and content and passes it into the display function
            const section = btn.id.replace("_btn", "");
            display(section, btn);
        });
    });

init();
console.log("Dashboard successfully loaded");
});

