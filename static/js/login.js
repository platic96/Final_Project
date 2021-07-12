function login() {
    const login = document.getElementById('loginRecordTag');
    const audio = document.createElement('audio');
    audio.autoplay = true;
    audio.controls = 'controls';
    audio.src = 'static/audio/login.wav';
    audio.type = 'audioio/ogg';
    audio.style = 'display:none;';
    login.appendChild(audio);
}

window.addEventListener('load',function() {
    record("loginRecordTag", "startTagl", "stopTagl", "mic1", "login");
    login();
    document.getElementById('startTagl').click();
    var loginbtn = document.getElementById('loginRecordTag');
    loginbtn.addEventListener('click', () => {
        document.getElementById('startTagl').click();
        setTimeout(() => document.getElementById('stopTagl').click(),5000);
    }, false);
});
