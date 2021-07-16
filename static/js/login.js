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
    record("loginRecordTag", "startTagl", "stopTagl", "mic1", login);
    login();
    // var loginbtn = document.getElementById('loginRecordTag');
    // var loginStartBtn = this.document.getElementById('startTagl')
    // var loginStopBtn = this.document.getElementById('stopTagl');
    // loginbtn.addEventListener('click', (e) => {
    //     loginStartBtn.click();
    //     e.stopPropagation()
    // }, false);
});