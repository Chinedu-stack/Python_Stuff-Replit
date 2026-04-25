import { display, init } from "./ui.js";





export async function loadDashboard() {     // this function fetches the html from the json files and then passes that content into the init function
    const response = await fetch('/static/DATA/data.json');  

    if (!response.ok) {
        console.log("Failed to load JSON:", response.status);
        return;
    }

    const content = await response.json();
    console.log("It works Nedu: " + content); // check if it loads
    init(content);
    return content
}


export async function fetch_tasks() { // this fetches the tasks from flask from the db
    const res = await fetch("/tasks");
    const data = await res.json()

    const tasks = [];

    data.forEach(item => {
        const task = {
            id: item.id,
            task: item.task,
            completed: item.is_done
        }
        tasks.push(task)
    })

    return tasks
    
    
}