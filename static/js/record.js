// record.js 함수화 필요
function record(divId, recordId, stopId, micId, login) {
	const record = document.createElement('button');
	record.classList.add('btn', 'btn-secondary');
	record.id = recordId;
	record.type = 'button';
	record.innerHTML = "녹음";
	if(login) {
		record.style.display = 'none';
	}

	const stop = document.createElement('button');
	stop.classList.add('btn', 'btn-secondary');
	stop.id = stopId;
	stop.type = 'button';
	stop.innerHTML = "정지";
	if(login) {
		stop.style.display = 'none';
	}
	

	const mic = document.createElement('button');
	mic.classList.add('form-check-input', 'btns', 'btn-info');
	mic.id = micId;
	mic.type = 'button';
	mic.innerHTML = '마이크';
	mic.style = 'display: none';

	divId = document.getElementById(divId);
	divId.append(record);
	divId.append(stop);
	divId.append(mic);

	const audioCtx = new (window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의
	const analyser = audioCtx.createAnalyser()

	function makeSound(stream) {
		const source = audioCtx.createMediaStreamSource(stream)
		source.connect(analyser)
		analyser.connect(audioCtx.destination)
	}


	if (navigator.mediaDevices) {
		const constraints = {
			audio: true
		}
		let chunks = []

		navigator.mediaDevices.getUserMedia(constraints)
			.then(stream => {

				const mediaRecorder = new MediaRecorder(stream)

				mic.onchange = e => {
					if (e.target.checked == true) {
						audioCtx.resume()
						makeSound(stream)
					} else {
						audioCtx.suspend()
					}
				}

				record.onclick = () => {
					mediaRecorder.start()
					console.log(mediaRecorder.state)
					if(login) {
						setTimeout(() => {
							mediaRecorder.stop()
						}, 5000);
					}
					record.style.background = "red"
					record.style.color = "black"
					
				}

				stop.onclick = () => {
					mediaRecorder.stop()
					console.log(mediaRecorder.state)
					record.style.background = ""
					record.style.color = ""
				}

				mediaRecorder.onstop = e => {
					const blob = new Blob(chunks, {
						'type': 'audio/ogg; codecs=opus'
					})

					chunks = []
					form_data = new FormData()
					var reader = new FileReader();
					var base64data;
					reader.readAsDataURL(blob);
					reader.onloadend = function () {
						base64data = reader.result
						form_data.append('base64', base64data)

						if(login) {
							url = "/login/";
						} else {
							url = "/talkBot/convwav"
						}

						$.ajax({
							url: url,
							type: 'POST',
							async: false,
							data: form_data,
							cache: false,
							processData: false, // essential
							contentType: false, // essential, application/pdf doesn't work.
							enctype: 'multipart/form-data',
							success: function (data) {
								if (data.message.length == 0) {
									setTimeout(function () {
										return sendMessage(['다시 입력해주세요.'], 'left');
									}, 1000);
								} else {
									setTimeout(() => {
										sendMessage(data.inputmessage, 'right')
										return sendMessage(data.message, 'left', data.path);
									}, 2000)
								}
							},
							error: function (request, status, error) {
								setTimeout(function () {
									return sendMessage(['죄송합니다. 서버 연결에 실패했습니다.'], 'left');
								}, 1000);
							}
						});
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
}