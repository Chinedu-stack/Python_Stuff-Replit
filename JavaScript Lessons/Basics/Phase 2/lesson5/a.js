 const tasks = [
    {title: "maths", completed: true, subtasks: ["algebra", "linear graphs", "cosine rule"]},
    {title: "english", completed: false, subtasks: ["poetry", "creative writing", "plays"]},
    {title: "geo", completed: true, subtasks: ["rocks", "informal", "economy", "sectors"]}
 ];





 
 for (const task of tasks) {
    console.log(`Topic: ${task.title} |  Completed: ${task.completed}  | Subtasks: ${task.subtasks.join(", ")}`);
 }

 for (const task of tasks) {
    if (!task.completed) {
        console.log(`${task.title} has not been completed.`);
    } else {
        console.log(`${task.title} has been completed.`);
    }
 }