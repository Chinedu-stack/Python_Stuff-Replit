import { loadDashboard } from "./api.js";
import { display } from "./ui.js";

const content = loadDashboard()  // this is the html content from the json files


document.addEventListener("DOMContentLoaded", async () => {
    const content =  await loadDashboard();
    console.log("Content loaded:", content)

    document.querySelectorAll("nav button").forEach(btn => {  // this runs the display function each time one of the nav buttons is being clicked 
        btn.addEventListener("click", () => {                 // it gets the section name, the btn and content and passes it into the display function
            const section = btn.id.replace("_btn", "");
            display(section, btn, content);
        });
    });
});

