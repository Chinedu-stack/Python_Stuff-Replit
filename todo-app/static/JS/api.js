import { display, init } from "./ui.js";


let content = {};
let tasks = {};

export async function loadDashboard() {     // this function fetches the html from the json files and then passes that content into the init function
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


export function fetch_tasks() { // this fetches the tasks from flask from the db
    fetch("/tasks")
    .then(res => res.json())
    .then(data => {
        data.forEach(task => {
            let task = {"task":task["task"], "completed":task["is_done"]};
            tasks[task.id] = task

        })
      console.log("Tasks successfully fetched");
      return tasks;  
    })
    
}