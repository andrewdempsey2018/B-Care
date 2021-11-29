// ----------- Modal for stories page

// Get the modal
const modal = document.getElementById("modal");

// Get the button that opens the modal
const delete_buttons = document.getElementsByClassName("delete_button");
const cancel_button = document.getElementById("cancel_button");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

let modal_target = "";

// When the user clicks on the button, open the modal
Array.from(delete_buttons).forEach(button => {
  button.onclick = () => {
    modal_target = button.getAttribute('data-story');
    document.getElementById('modal_delete_button').setAttribute('href', "delete_story?" + "storyId=" + modal_target);
    modal.style.display = "block";
  }
})

cancel_button.onclick = () => {
  modal.style.display = "none";
}

span.onclick = () => {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = (event) => {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// ----------- Specific modal code for admin page

const delete_buttons_admin = document.getElementsByClassName("delete_button_admin");

Array.from(delete_buttons_admin).forEach(button => {
  button.onclick = () => {
    modal_target = button.getAttribute('data-admin');
    document.getElementById('modal_delete_button').setAttribute('href', "delete_admin?" + "userId=" + modal_target);
    modal.style.display = "block";
  }
})