const list = document.getElementById("list");




function display() {

    fetch("/tasks")
        .then(res => res.json())
        .then(data => {

            list.innerHTML = "";

            data.forEach(task => {
                const li = document.createElement("li");

                li.innerHTML = `
                    ${task.text}
                    <button onclick="deleteTask(${task.id}, '${task.text}')">❌</button>
                `;

                list.appendChild(li);
                console.log("The fetch to display has worked")
            });

        });
}

function deleteTask(id, text) {
    console.log(`This has been deleted: ${text}\nID: ${id}`);
    
        fetch("/delete_task", {
        method: "POST",
        headers : {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            id: id
        })

    })

    .then(res => res.json())
    .then(data => {
        if (data.success) {
            display()
            console.log("The fetch to delete has worked");
        }
        else {
            console.log("Delete Failed on the backend")
        }
        
    });



};

display();