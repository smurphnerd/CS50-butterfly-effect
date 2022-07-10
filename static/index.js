const element = document.querySelector('#myUL');
const user = document.getElementById('user-id').innerHTML;
fetch("static/user_data/user" + user + ".json").then(async response => {
    response = await response.json();
    displayTree(response);
    addCaretListeners();
    addEffectListeners();
    addConsequence();
    editMessage();
    deleteEffect();
    addRootListeners();
    changeDefault();
})
    .catch(error => {
        element.innerHTML += `${error}`;
    });


const textColors = [
    '#cccccc',
    '#9cdcf1',
    '#ce9178',
    '#dcdcaa',
    '#6a9953',
    '#c586c0',
    '#4ec9b0',
    '#569cd6',
    '#ffd710'
];
const lenColors = textColors.length;

function displayTree(response, parent = element, tier = 0) {
    // Create a node and assign it to its parent
    const node = document.createElement('li');
    const div = document.createElement('div');
    const tierLine = document.createElement('div');
    node.className = 'root-node';
    div.id = `${response['id']}`
    div.className = 'node node-untoggled';
    div.innerHTML = `${response['message']}`;
    node.appendChild(div);
    parent.appendChild(node);

    // Change the div color based on tier
    let nodeColor = textColors[tier % lenColors]
    node.style.color = nodeColor;

    // If the node has children, recursively add them
    if (response['children']) {
        tier++;
        // Create a new list inside the current node
        const caret = document.createElement('span');
        caret.className = 'caret caret-down';
        tierLine.className = 'tier-line nested active';
        tierLine.style.background = nodeColor;
        node.appendChild(tierLine);
        div.prepend(caret);

        const newRoot = document.createElement('ul');
        newRoot.className = 'nested active';
        node.appendChild(newRoot)
        // Add each child to the new node
        for (child of response['children']) {
            displayTree(child, newRoot, tier);
        }
    }
    return
}


function addCaretListeners() {
    // https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_treeview
    var toggler = document.getElementsByClassName("caret");
    var i;
    let len = toggler.length

    for (i = 0; i < len; i++) {
        toggler[i].addEventListener("click", function () {
            this.parentElement.parentElement.querySelectorAll(".nested").forEach(x =>
                x.classList.toggle("active"));
            this.classList.toggle("caret-down");
        });
    }
}


// Add highlight functionality for list items
function addEffectListeners() {
    let body = document.querySelector("body")

    var nodes = document.querySelectorAll(".node");
    var i;
    let len = nodes.length;

    // Deslect the node if the body is clicked
    body.addEventListener("click", function (e) {
        if (!e.target.classList.contains('node-toggled')) {
            document.querySelector(".node-toggled").className = "node node-untoggled";
        }
    });

    // Change class if node is clicked
    for (i = 0; i < len; i++) {
        nodes[i].addEventListener("click", function () {
            for (j = 0; j < len; j++) {
                nodes[j].className = "node node-untoggled"
            }
            this.className = "node node-toggled";
        });
    }
}


// Change default root
function addConsequence() {
    document.querySelector("#add-consequence-btn").addEventListener("click", function () {
        // Get the selected node's id
        let div = document.querySelector(".node-toggled");
        if (div == null) {
            alert('No node have been selected! :p');
            return
        }
        // Open the pop-up form
        document.querySelector(".pop-up-forms").style.display = "block";
        document.querySelector("#add-child").style.display = "flex";

        // Add the parent's id
        document.querySelector('#add-child-id').value = div.id;
    });
}


// Edit a node's message
function editMessage() {
    document.querySelector("#edit-message-btn").addEventListener("click", function () {
        // Get the selected node's id
        let div = document.querySelector(".node-toggled");
        if (div == null) {
            alert('No node have been selected! :p');
            return
        }
        // Get the node's id
        document.querySelector('#edit-message-id').value = div.id;

        // Add the former message to the text area
        let message = div.textContent;
        document.querySelector('#edit-message-ta').innerHTML = message;

        // Open the pop-up form
        document.querySelector(".pop-up-forms").style.display = "block";
        document.querySelector("#edit-message").style.display = "flex";
    });
}


// Change default root
function deleteEffect() {
    document.querySelector("#delete-effect-btn").addEventListener("click", function () {
        // Get the invis form
        const form = document.querySelector("#invis-form");
        // Get the selected node's id
        let div = document.querySelector(".node-toggled");
        if (div == null) {
            alert('No node has been selected! :p');
            return
        }
        const id = div.id;
        // Add values to a new input element
        const idInput = document.createElement("input");
        idInput.name = 'node-id';
        idInput.value = id;
        // Add the type to a new input element
        const typeInput = document.createElement("input");
        typeInput.name = 'delete-node';

        // Append new elements to the invis form
        form.appendChild(idInput);
        form.appendChild(typeInput);

        // Submit the form
        form.submit();
    });
}


function addRootListeners() {
    let body = document.querySelector("body")

    var toggler = document.querySelectorAll(".root-item");
    var i;
    let len = toggler.length;

    // Deslect the root toggler if the body is clicked
    body.addEventListener("click", function (e) {
        if (!e.target.classList.contains('root-item-toggled')) {
            document.querySelector(".root-item-toggled").className = "root-item root-item-untoggled";
        }
    });

    // Change class if root is clicked
    for (i = 0; i < len; i++) {
        toggler[i].addEventListener("click", function () {
            for (j = 0; j < len; j++) {
                toggler[j].className = "root-item root-item-untoggled"
            }
            this.className = "root-item root-item-toggled";
        });
    }
}


// Change default root
function changeDefault() {
    document.querySelector(".set-default-btn").addEventListener("click", function () {
        // Get the invis form
        const form = document.querySelector("#invis-form");
        // Get the selected node's id
        let div = document.querySelector(".root-item-toggled");
        if (div == null) {
            alert('No effects have been selected! :p');
            return
        }
        const id = div.id;
        // Add values to a new input element
        const idInput = document.createElement("input");
        idInput.name = 'node-id';
        idInput.value = id;
        // Add the type to a new input element
        const typeInput = document.createElement("input");
        typeInput.name = 'root-session';

        // Append new elements to the invis form
        form.appendChild(idInput);
        form.appendChild(typeInput);

        // Submit the form
        form.submit();
    });
}


// Exit button functionality
function sidebarBtn() {
    var exitBtn = document.querySelectorAll(".exit-btn");

    for (i = 0; i < 2; i++) {
        exitBtn[i].addEventListener("mouseover", function (e) {
            e.target.src = "/static/images/exit-white.png";
        });
        exitBtn[i].addEventListener("mouseout", function (e) {
            e.target.src = "/static/images/exit-grey.png";
        });
    }

    document.getElementById("exit-btn-close").addEventListener("click", function () {
        document.querySelector(".sidebar").style.width = 0;
        document.querySelector(".main-content").style.marginLeft = "2.5vw";
        document.querySelector(".closed-sidebar").style.width = "2.5vw";
    });

    document.getElementById("exit-btn-open").addEventListener("click", function () {
        document.querySelector(".sidebar").style.width = "18vw";
        document.querySelector(".main-content").style.marginLeft = "18vw";
        document.querySelector(".closed-sidebar").style.width = 0;
    });
}


// Pop up form open and close
function popUpForm() {
    document.querySelector("#add-effect-btn").addEventListener("click", function () {
        document.querySelector(".pop-up-forms").style.display = "block";
        document.querySelector("#add-root").style.display = "flex";
    });

    document.querySelector(".exit-pop-up-btn").addEventListener("click", function () {
        document.querySelector(".pop-up-forms").style.display = "none";
        document.querySelector("#add-root").style.display = "none";
        document.querySelector("#add-child").style.display = "none";
        document.querySelector("#add-message").style.display = "none";
    })
}


sidebarBtn();
popUpForm();

// https://www.developer.com/design/creating-a-tree-diagram-with-d3-js/