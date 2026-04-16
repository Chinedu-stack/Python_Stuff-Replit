fetch("/add-user", {
    method : "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name:"Chinedu",
        age: 14
    })
})