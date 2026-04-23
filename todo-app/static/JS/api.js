import { display, init } from "./ui.js";


let content = {};

export async function loadDashboard() {
    const response = await fetch('/static/DATA/data.json');

    if (!response.ok) {
        console.log("Failed to load JSON:", response.status);
        return;
    }

    content = await response.json();
    console.log("It works Nedu: " + content); // check if it loads
    init(content);
    return content
}