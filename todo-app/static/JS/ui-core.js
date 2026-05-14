export function showMsg(message, color) {
    const msg_list = document.getElementById("msg_list");

    msg_list.style.color = color;
    msg_list.textContent = "";

    if (Array.isArray(message)) {
        message.forEach(function(msg_element) {
            const li = document.createElement("li");
            li.textContent = msg_element;
            msg_list.appendChild(li);
        })
    } else {
        const li = document.createElement("li");
        li.textContent = message;
        msg_list.appendChild(li);
    }

    setTimeout(() => {
        msg_list.textContent = "";
    }, 1000);
}

export function check_date(end_date) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const date = new Date(end_date);

    if (date < today) {
        return true;
    } else {
        return false;
    }
}