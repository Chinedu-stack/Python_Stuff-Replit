import { display, init } from "./ui.js";


export async function fetch_tasks() { // this fetches the tasks from flask from the db
    const res = await fetch("/fetch_tasks");
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
    console.log("tasks fetch successfully");

    return tasks
    
    
}


async function add_task(task) {
    fetch("/add_tasks", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task: task
        })
    })

    
}