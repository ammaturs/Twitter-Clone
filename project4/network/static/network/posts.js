
document.addEventListener('DOMContentLoaded', function() {

    //get all edit buttons on document
    const editButtons = document.querySelectorAll('.edit-button');

    //loop through all posts, addEvenetListener to each edit button and get the id of the edit button thats clicked
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Extract the postId from the data-post-id attribute of the button
            const editPostId = button.getAttribute('data-post-id');
            edit(editPostId);
        });
    });//forEach closer

    const saveButtons = document.querySelectorAll('.save-button');

    //loop through all posts, addEvenetListener to each save button and get the id of the save button thats clicked
    saveButtons.forEach(button => {
        button.addEventListener('click', () => {
            const savePostId = button.getAttribute('data-post-id');
            save(savePostId);
        });
    });//forEach closer

    const likeButtons = document.querySelectorAll('.like-button');

    //loop through all posts, addEvenetListener to each like button and get the id of the like button thats clicked
    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const new_like_postId = button.getAttribute('data-post-id');
            like(new_like_postId);
        });
    });//forEach closer


})//eventListener closer

function edit(postId)
{

    //if edit button click, hide post-content and show textarea, hide edit button show save button
    document.querySelector(`#post-content-${postId}`).style.display = 'none';
    document.querySelector(`#text-area-${postId}`).style.display = 'block';
    document.querySelector(`[data-post-id="${postId}"].edit-button`).style.display='none';
    document.querySelector(`[data-post-id="${postId}"].save-button`).style.display='block';

}//function closer

function save(postId)
{

    let new_content = document.querySelector(`#text-area-${postId}`).value;

    const csrfToken = document.querySelector(`#text-area-${postId}`).getAttribute('data-csrf');

    // Include the CSRF token in the request headers
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // Include the CSRF token here
    });


    fetch(`/edit/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            new_content: new_content
        }),
        headers: headers  // Include the headers in the fetch request
    })
    .then(response => response.json())
    .then(result => {

        document.querySelector(`#post-content-${postId}`).textContent = new_content;

        document.querySelector(`#post-content-${postId}`).style.display = 'block';
        document.querySelector(`#text-area-${postId}`).style.display = 'none';
        document.querySelector(`[data-post-id="${postId}"].edit-button`).style.display='block';
        document.querySelector(`[data-post-id="${postId}"].save-button`).style.display='none';
    })//then result closer
}//function closer

function like(postId)
{
    const csrfToken = document.querySelector(`#like-button-${postId}`).getAttribute('data-csrf');

    // Include the CSRF token in the request headers
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // Include the CSRF token here
    });

    fetch(`/like/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            new_like:'yes'
        }),
        headers: headers
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector(`#like-count-${postId}`).textContent = result.likes;
    })
}//function closer



//ADD EDIT SAVE AND LIKE FUNCTIONALITY TO OTHER PAGES