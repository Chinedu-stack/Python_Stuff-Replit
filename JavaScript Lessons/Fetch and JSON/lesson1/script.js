fetch("/api/tasks")
  .then(res => {
    if (!res.ok) {
        throw new Error("Failed request");
    }
    return res.json();

  })
  .then(data => {
        console.log(data);
  })
  .catch(err => {
    console.log(`Caught: ${err.message}`);
  });
  