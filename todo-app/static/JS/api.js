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
    console.log("tasks fetched successfully");

    return tasks
    
    
}


export async function add_task(task_name) {
    const res =  await fetch("/add_tasks", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify(task_name)
    })

   const response = await res.json()

   if (response.success) {
    console.log("Task added")
   }

    
}


export async function delete_task(task_name) {
    const res = await fetch("/delete_tasks", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task: task_name
        })
    })

    const response = await res.json()

    if (response.success) {
    console.log("Task deleted from DB")
   }
}

export async function edit_task(task, new_task) {
    const res = await fetch("/edit_task", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task: task,
            new_task: new_task
        })
    })

    const response = await res.json()

    if (response.success) {
        console.log("Task edited")
    }
}

export async function task_done(task_name) {
    const res = await fetch("/task_done", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task: task_name
        })
    })

    const response = await res.json()

    if (response.success) {
        console.log("Task marked as done")
    }
}