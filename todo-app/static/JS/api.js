import { display, init } from "./ui.js";


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