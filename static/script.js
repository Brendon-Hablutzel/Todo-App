
document.getElementById("add-todo-button").addEventListener("click", () => {
    document.getElementById("add-todo-modal").style['display'] = "block";
});


document.getElementById("close-modal").addEventListener("click", () => {
    document.getElementById("add-todo-modal").style['display'] = "none";
});

document.getElementById("add-todo-submit").addEventListener("click", () => {
    let name = document.getElementById("add-todo-name").value;
    let value = document.getElementById("add-todo-value").value;
    let category = document.getElementById("add-todo-category").value;
    if (name && value && category) {
        document.getElementById("add-todo-modal").style['display'] = "none";
    } else {
        alert("Please fill out all information");
    }
});
