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

