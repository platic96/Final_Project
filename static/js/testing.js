window.onload = function(){
    const record = document.getElementById("record")
    const stop = document.getElementById("stop")
    const soundClips = document.getElementById("sound-clips")
    // var chkHearMic = document.getElementById("chk-hear-mic")
    var audioCtx = null;
    var analyser = null;

    //        const distortion = audioCtx.createWaveShaper()
    //        const gainNode = audioCtx.createGain()
    //        const biquadFilter = audioCtx.createBiquadFilter()



    console.log("navigator : "+navigator.mediaDevices)
    if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
    }


    if (navigator.mediaDevices) {
        console.log('getUserMedia supported.')

        const constraints = {
            audio: true
        }
        let chunks = []

        if (navigator.mediaDevices.getUserMedia === undefined) {
            navigator.mediaDevices.getUserMedia = function(constraints) {

                // First get ahold of the legacy getUserMedia, if present
                var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

                // Some browsers just don't implement it - return a rejected promise with an error
                // to keep a consistent interface
                if (!getUserMedia) {
                    return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
                }

                // Otherwise, wrap the call to the old navigator.getUserMedia with a Promise
                return new Promise(function(resolve, reject) {
                    getUserMedia.call(navigator, constraints, resolve, reject);
                });
            }
        }


        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {

                const mediaRecorder = new MediaRecorder(stream)


                // chkHearMic.onchange = e => {
                //     console.log("1")
                //     if (audioCtx == null ){
                //         audioCtx = new(window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의
                //         analyser = audioCtx.createAnalyser()
                //         console.log("2")
                //     }

                //     if(e.target.checked == true ) {
                //         console.log("3")
                //         audioCtx.resume()
                //         makeSound(stream)
                //         console.log("4")
                //     } else {
                //         console.log("5")
                //         audioCtx.suspend()
                //         console.log("6")
                //     }
                // }

                record.onclick = () => {
                    if (audioCtx == null ){
                        audioCtx = new(window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의
                        analyser = audioCtx.createAnalyser()
                    }
                    audioCtx.resume()
                    mediaRecorder.start()
                    console.log(mediaRecorder.state)
                    console.log("recorder started")
                    record.style.background = "red"
                    record.style.color = "black"
                }

                stop.onclick = () => {
                    if (audioCtx == null ){
                        audioCtx = new(window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의
                       analyser = audioCtx.createAnalyser()
                    }
                    audioCtx.resume()
                    mediaRecorder.stop()
                    console.log(mediaRecorder.state)
                    console.log("recorder stopped")
                    record.style.background = ""
                    record.style.color = ""
                }

                mediaRecorder.onstop = e => {
                    console.log("data available after MediaRecorder.stop() called.")
                    const clipName = prompt("오디오 파일 제목을 입력하세요.", new Date())

                    const clipContainer = document.createElement('article')
                    const clipLabel = document.createElement('p')
                    const audio = document.createElement('audio')
                    const deleteButton = document.createElement('button')

                    clipContainer.classList.add('clip')
                    audio.setAttribute('controls', '')
                    deleteButton.innerHTML = "삭제"
                    clipLabel.innerHTML = clipName

                    clipContainer.appendChild(audio)
                    clipContainer.appendChild(clipLabel)
                    clipContainer.appendChild(deleteButton)
                    soundClips.appendChild(clipContainer)

                    audio.controls = true
                    const blob = new Blob(chunks, {
                        'type': 'audio/webm; codecs=opus'
                    })
                    console.log(blob)
                    chunks = []
                    const audioURL = URL.createObjectURL(blob)
                    audio.src = audioURL

                    audio_name = getToday() + '_' + guid();

                    form_data = new FormData()
                    form_data.append('name', audio_name + '.wav')
                    form_data.append('audio', blob)

                    // ajax 통신(시작)
                    $.ajax({
                        url: 'ajax_method/',
                        type: 'POST',
                        headers: { 'X-CSRFToken': '{{ csrf_token() }}' },
                        data: form_data,
                        cache: false,
                        processData: false, // essential
                        contentType: false, // essential, application/pdf doesn't work.
                        enctype: 'multipart/form-data',
                        success: function(result) {
                            // first = encodeURIComponent(result.file)
                            // new_blob = b64toBlob(first, 'audio/webm; codecs=opus')
                            // new_audioURL = URL.createObjectURL(new_blob)
                            alert(result.file);
                            alert(result.message);

                            audio_print(result.file, $message, $messages, result.message);
                        },
                    });

                    // 화면에 오디오 출력해주기(시작)
                    $message = $($('.template_outgoing').clone().html());
                    let $messages = $('.msg_history');
                    // 화면에 오디오 출력해주기(끝)

                    console.log("recorder stopped");

                    deleteButton.onclick = e => {
                        evtTgt = e.target
                        evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode)
                    }
                }

                mediaRecorder.ondataavailable = e => {
                    chunks.push(e.data)
                }
            })
            .catch(err => {
                console.log('The following error occurred: ' + err)
            })
    }else {
        console.log("현재 사용 중인 브라우저의 버전 정보는 " + navigator.appVersion + "입니다.<br><br>");
        console.log("userAgent 프로퍼티로 알 수 있는 추가 정보는 " + navigator.userAgent + "입니다.");
    }

}

function makeSound(stream) {
    console.log("function makeSound")
    const source = audioCtx.createMediaStreamSource(stream)

    source.connect(analyser)
    //            analyser.connect(distortion)
    //            distortion.connect(biquadFilter)
    //            biquadFilter.connect(gainNode)
    //            gainNode.connect(audioCtx.destination) // connecting the different audio graph nodes together
    analyser.connect(audioCtx.destination)

}


function getToday(){
    var date = new Date();
    var year = date.getFullYear();
    var month = ("0" + (1 + date.getMonth())).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);

    return year + month + day;
}


function audio_print(new_audioURL, $message, $messages, voice_text) {
    const aud = document.createElement('audio')
    aud.controls = 'controls'
    aud.src = new_audioURL
    aud.type = 'audio/ogg'

    const audio_text = document.createElement('p')
    audio_text.textContent = voice_text
    $message.find('p.content').append(audio_text)
    $message.find('p.content').append(aud)
    $message.find('span.time_date').text(getTimeStamp())
    $('.msg_history').append($message)
    $messages.animate({scrollTop: $messages.prop('scrollHeight')}, 300);
}


function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data);
    blob = decodeURIComponent(byteCharacters);
    console.log(blob);
    // var byteArrays = [];

    // for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    //     var slice = byteCharacters.slice(offset, offset + sliceSize);

    //     var byteNumbers = new Array(slice.length);
    //     for (var i = 0; i < slice.length; i++) {
    //         byteNumbers[i] = slice.charCodeAt(i);
    //     }

    //     var byteArray = new Uint8Array(byteNumbers);

    //     byteArrays.push(byteArray);
    // }

    // var blob = new Blob(byteArrays, {type: contentType});
    // console.log(blob)
    return blob;
}

function guid() {
    function s4() {
        return ((1 + Math.random()) * 0x10000 | 0).toString(16).substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}