const element = document.querySelector('ul');
const user = document.getElementById('user-id').innerHTML;
console.log(user);
fetch("static/user_data/user" + user + ".json").then(async response => {
    response = await response.json();
    displayTree(response);

    // https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_treeview
    var toggler = document.getElementsByClassName("caret");
    var i;
    let len = toggler.length

    for (i = 0; i < len; i++) {
        toggler[i].addEventListener("click", function () {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        });
    }
})
    .catch(error => {
        element.innerHTML += `${error}`;
    });


function displayTree(response, parent = element) {
    // Create a node and assign it to its parent
    const node = document.createElement('li');
    node.innerHTML = `${response['id']} ${response['message']}`;
    parent.appendChild(node)

    // If the node has children, recursively add them
    if (response['children']) {
        // Create a new list inside the current node
        const caret = document.createElement('span');
        caret.className = 'caret';
        node.prepend(caret);

        const newRoot = document.createElement('ul');
        newRoot.className = 'nested';
        node.appendChild(newRoot)
        // Add each child to the new node
        for (child of response['children']) {
            console.log(child['id']);
            displayTree(child, newRoot);
        }
    }
    return
}
// https://www.developer.com/design/creating-a-tree-diagram-with-d3-js/