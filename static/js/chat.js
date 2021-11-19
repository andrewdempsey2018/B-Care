/* create a socket on the client */
let socket = io();

let message = document.getElementById('messageField');
let username = document.getElementById('username');
let sendButton = document.getElementById('sendButton');

let message_area = document.getElementById('message_area');

let ping = new Audio('../static/audio/ping.wav');

/* user clicks submit button, socket sends the message to the server */
sendButton.addEventListener('click', e => {
    e.preventDefault();
    console.log(message.value);
    /* send the text 'message' to the server. The server is listening for this exact text
       upon receiving 'message', the corresponding method will fire */
    socket.emit('message', username.value + ': ' + message.value);
    message.value = "";
});

/* server has sent the text 'updateui' to the client
   along with the text message to be displayed
   UI is then updated */
socket.on('updateui', data => {
    message_area.innerHTML = '<br>' + data + message_area.innerHTML;
    //message_area.innerHTML += data + '<br>';
    ping.play();
})

/* Send a message with enter key */
window.addEventListener('keydown', (key) => {
    if (key.keyCode === 13) {
        console.log(message.value);
        /* send the text 'message' to the server. The server is listening for this exact text
           upon receiving 'message', the corresponding method will fire */
        socket.emit('message', username.value + ': ' + message.value);
        message.value = "";
    }
}, false);

/*Andrew's woman in tech... For my woman in tech I'd like to nominate Abi Harrison,
a UI developer at giffgaff, public speaker, blogger and musician. Abi is a super
skilled coder with lots of neat tricks up her sleeve but more than that...
she shows what true diversity in the tech sector is all about -
she brings her caring and supportive spirit to all those who share her passion!
Long live The Zombie King!!!! */

