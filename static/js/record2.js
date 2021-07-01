const record = document.getElementById("record")
const stop = document.getElementById("stop")
const soundClips = document.getElementById("sound-clips")
const chkHearMic = document.getElementById("chk-hear-mic")

const audioCtx = new(window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의

const analyser = audioCtx.createAnalyser()
//		const distortion = audioCtx.createWaveShaper()
//		const gainNode = audioCtx.createGain()
//		const biquadFilter = audioCtx.createBiquadFilter()

function makeSound(stream) {
	const source = audioCtx.createMediaStreamSource(stream)

	source.connect(analyser)
	//			analyser.connect(distortion)
	//			distortion.connect(biquadFilter)
	//			biquadFilter.connect(gainNode)
	//			gainNode.connect(audioCtx.destination) // connecting the different audio graph nodes together
	analyser.connect(audioCtx.destination)

}

function getToday(){
    var date = new Date();
    var year = date.getFullYear();
    var month = ("0" + (1 + date.getMonth())).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);

    return year + month + day;
}

if (navigator.mediaDevices) {
	console.log('getUserMedia supported.')

	const constraints = {
		audio: true
	}
	let chunks = []

	navigator.mediaDevices.getUserMedia(constraints)
		.then(stream => {

			const mediaRecorder = new MediaRecorder(stream)

			chkHearMic.onchange = e => {
				if(e.target.checked == true) {
					audioCtx.resume()
					makeSound(stream)
				} else {
					audioCtx.suspend()
				}
			}

			record.onclick = () => {
				mediaRecorder.start()
				console.log(mediaRecorder.state)
				console.log("recorder started")
				record.style.background = "red"
				record.style.color = "black"
			}

			stop.onclick = () => {
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
				chunks = []
				const audioURL = URL.createObjectURL(blob)
				audio.src = audioURL

				audio_name = getToday();

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
				alert(result.message);
				alert(result.file)
				//audio_print(response.file, $message, $messages, response.success);
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
}
