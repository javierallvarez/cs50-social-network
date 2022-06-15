

document.addEventListener('DOMContentLoaded', function() {
    // Pass as variable a css class:
    const delPost = document.querySelectorAll('.delete')
    // Click to delete via deletePost function:
    delPost.forEach(element => {
        element.addEventListener('click', () => {
            deletePost(element);
        })
    })

    const like = document.querySelectorAll('.like');
    like.forEach(element => {
        element.addEventListener('click', () => {
            likePost(element);
        });
    })

    const unlike = document.querySelectorAll('.unlike');
    unlike.forEach(element => {
        element.addEventListener('click', () => {
            unlikePost(element);
        })
    })

    const edit = document.querySelectorAll('.edit');
    edit.forEach(element => {
        element.addEventListener('click', () => {
            editView(element);
        });
    });
});


// ---------------DELETE------------------



// Hide the alert message, set to 2000 miliseconds above.
function alertMsg(){
    let alert_message = document.querySelector('#alert_message');
    alert_message.style.display = 'none';
}


function deletePost(element) {
    let id = element.getAttribute("data-id");
    let comment = document.querySelector(`#comment-${id}`);
    let alert_message = document.querySelector('#alert_message');
    let avatar = document.querySelector(`#avatar-${id}`);
    // Create a keyword form via FormData to find the post's id:
    const form = new FormData();
    form.append("id", id);
    // Create an alert with the confirm() function:
    let alert = confirm("Are you sure to delete this?");
    // Send a get request to the url and the information is stored via post request.
    if (alert == true) {
        fetch("/delete/", {
            method: 'POST',
            body: form
        })
        // Change the display of the elements to none and show the confirmation message:
        .then(res => res.json())
        .then(res => {
            console.log(res)
            if(avatar){
                avatar.style.display = 'none';
            }
            comment.style.display = 'none';
            alert_message.style.display = 'block';
            alert_message.innerHTML = 
                    `<div class="alert-msg" role="alert">
                        Post deleted succesfully. 
                    </div>`;
                    setTimeout('alertMsg()', 2000);
        });
    }
}


// ---------------EDIT------------------


// Create the form where the post will be edited:
function editPost(id, post) {
    let editedPost = new FormData()
    editedPost.append("id", id);
    editedPost.append("post", post);
    fetch("/edit/", {
        method: "POST",
        body: editedPost
    })
    .then((res) => {
        console.log(res.status)
        document.querySelector(`#postView-${id}`).textContent = post;
        document.querySelector(`#postView-${id}`).style.display = "block";
        document.querySelector(`#editView-${id}`).style.display = "none";
        document.querySelector(`#editView-${id}`).value = post;
    });
}

function editView(element) {
    // Get the id of the selected element:
    let id = element.getAttribute("data-id");
    let editView = document.querySelector(`#editView-${id}`); 
    let postView = document.querySelector(`#postView-${id}`);
    // Hide the real post and show the edit view:
    editView.style.display = 'flex'; 
    postView.style.display = 'none';
    // Create the Cancel button and hide the edit view:
    let cancelButton = document.querySelector(`#cancel-${id}`);
    cancelButton.addEventListener('click', () => { 
        editView.style.display = 'none'; 
        postView.style.display = 'block';
    });
    // Create the Save button:
    let saveButton = document.querySelector(`#save-${id}`);
    saveButton.addEventListener('click', () => {
        editPost(id, document.querySelector(`#content-${id}`).value)
    });
}


// ---------------LIKE/UNLIKE------------------


function likePost(element) {
    let id = element.getAttribute("data-id");
    let likeButton = document.querySelector(`#likePost-${id}`);
    const form = new FormData();
    form.append("id", id);
    fetch("/like/", {
        method: 'POST',
        body: form
    })
    .then(res => res.json())
    .then(res => {
        document.querySelector(`#postLikes-${id}`).textContent = res.count;
        likeButton.classList.toggle("turq");
        // likeButton.classList.add("turq") 
    })
}


function unlikePost(element) {
    let id = element.getAttribute("data-id");
    let unlikeButton = document.querySelector(`#unlikePost-${id}`);
    const form = new FormData();
    form.append("id", id);
    fetch("/like/", {
        method: "POST",
        body: form
    })
    .then(res => res.json())
    .then(res => {
        document.querySelector(`#postLikes-${id}`).textContent = res.count;
        unlikeButton.classList.toggle("turq"); 
        // unlikeButton.classList.add("blu")
    });
}


// ---------------BURGUER-MENU------------------

let theToggle = document.getElementById('toggle');

// hasClass
function hasClass(elem, className) {
	return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
}
// addClass
function addClass(elem, className) {
    if (!hasClass(elem, className)) {
    	elem.className += ' ' + className;
    }
}
// removeClass
function removeClass(elem, className) {
	var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ') + ' ';
	if (hasClass(elem, className)) {
        while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
            newClass = newClass.replace(' ' + className + ' ', ' ');
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    }
}
// toggleClass
function toggleClass(elem, className) {
	var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, " " ) + ' ';
    if (hasClass(elem, className)) {
        while (newClass.indexOf(" " + className + " ") >= 0 ) {
            newClass = newClass.replace( " " + className + " " , " " );
        }
        elem.className = newClass.replace(/^\s+|\s+$/g, '');
    } else {
        elem.className += ' ' + className;
    }
}

theToggle.onclick = function() {
   toggleClass(this, 'on');
   return false;
}