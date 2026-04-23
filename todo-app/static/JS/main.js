import { loadDashboard } from "./api.js";
import { display } from "./ui.js";

const content = loadDashboard()


document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();

    document.querySelectorAll("nav button").forEach(btn => {
        btn.addEventListener("click", () => {
            const section = btn.id.replace("_btn", "");
            display(section, btn, content);
        });
    });
});

