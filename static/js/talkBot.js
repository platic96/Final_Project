// // variables
// let userName = null;
// let state = 'SUCCESS';

// // functions
// function Message(arg) {
//     this.text = arg.text;
//     this.message_side = arg.message_side;

//     this.draw = function (_this) {
//         return function () {
//             let $message;
//             $message = $($('.message_template').clone().html());
//             $message.addClass(_this.message_side).find('.text').html(_this.text);
//             $('.messages').append($message);

//             return setTimeout(function () {
//                 return $message.addClass('appeared');
//             }, 0);
//         };
//     }(this);
//     return this;
// }

// function getMessageText() {
//     let $message_input;
//     $message_input = $('.message_input');
//     return $message_input.val();
// }

// function sendMessage(text, message_side) {
//     let $messages, message;
//     $('.message_input').val('');
//     $messages = $('.messages');
//     message = new Message({
//         text: text,
//         message_side: message_side
//     });
//     message.draw();
//     $messages.animate({scrollTop: $messages.prop('scrollHeight')}, 300);
// }

// function greet() {
//     setTimeout(function () {
//         return sendMessage("Bit to BIT 채팅을 사용해주셔서 감사합니다.", 'left');
//     }, 1000);

//     setTimeout(function () {
//         return sendMessage("아이디를 입력해주세요.", 'left');
//     }, 2000);
// }

// function onClickAsEnter(e) {
//     if (e.keyCode === 13) {
//         onSendButtonClicked()
//     }
// }

// function setUserName(username) {

//     if (username != null && username.replace(" ", "" !== "")) {
//         setTimeout(function () {
//             return sendMessage("반갑습니다." + username + "님.", 'left');
//         }, 1000);
//         setTimeout(function () {
//             return sendMessage("저는 각종 가상화폐에 대한 정보를 알려주는 챗봇입니다.", 'left');
//         }, 2000);
//         setTimeout(function () {
//             return sendMessage("어떤 것을 알려드릴까요?", 'left');
//         }, 3000);
//         setTimeout(function () {
//             return sendMessage("1.투자 현황  2.자산 현황 3. 코인현황",'left');
//         }, 4000);

//         return username;

//     } else {
//         setTimeout(function () {
//             return sendMessage("올바른 프라이벳 키를 입력해주세요.", 'left');
//         }, 1000);

//         return null;
//     }
// }

// function requestChat(messageText, url_pattern) {
//     $.ajax({
//     	url: "http://127.0.0.1:80/" + url_pattern + '/' + userName + '/' + messageText,
//         //url: "http://0.0.0.0:8080/" + url_pattern + '/' + userName + '/' + messageText,
//         type: "GET",
//         dataType: "json",
//         success: function (data) {
//             state = data['state'];

//             if (state === 'SUCCESS') {
//                 return sendMessage(data['answer'], 'left');
//             } else if (state === 'REQUIRE_LOCATION') {
//                 return sendMessage('어느 지역을 알려드릴까요?', 'left');
//             } else {
//                 return sendMessage('죄송합니다. 무슨말인지 잘 모르겠어요.', 'left');
//             }
//         },

//         error: function (request, status, error) {
//             console.log(error);

//             return sendMessage('죄송합니다. 서버 연결에 실패했습니다.', 'left');
//         }
//     });
// }

// function onSendButtonClicked() {
//     let messageText = getMessageText();
//     sendMessage(messageText, 'right');

//     if (userName == null) {
//         userName = setUserName(messageText);

//     } else {
//         if (messageText.includes('안녕')) {
//             setTimeout(function () {
//                 return sendMessage("안녕하세요. 저는 Kochat 여행봇입니다.", 'left');
//             }, 1000);
//         } else if (messageText.includes('고마워')) {
//             setTimeout(function () {
//                 return sendMessage("천만에요. 더 물어보실 건 없나요?", 'left');
//             }, 1000);
//         } else if (messageText.includes('없어')) {
//             setTimeout(function () {
//                 return sendMessage("그렇군요. 알겠습니다!", 'left');
//             }, 1000);


//         } else if (state.includes('REQUIRE')) {
//             return requestChat(messageText, 'fill_slot');
//         } else {
//             return requestChat(messageText, 'request_chat');
//         }
//     }
// }


//////////////////////////////////////////////// NEW //////////////////////////////////////////////////////////////////////


// variables
let userName = null;
let state = 'SUCCESS';
var text_flag = true;
var conv_id = '';
var cur_bot = 'Talkbot';
var count = 0;
// functions

// 메세지 객체에 값 할당 함수
function Message(arg) {
    this.text = arg.text;
    this.message_side = arg.message_side;
    this.wavPath = arg.wavPath;

    this.draw = function (_this) {
        return function () {
            let $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(_this.text);
            $message[0].id = "mwav" + count++
            $('.messages').append($message);
            if (_this.wavPath != undefined) {
                // wav파일 추가
                const mwav = document.getElementById('mwav'+ (count-1))
                const audio = document.createElement('audio');
                audio.autoplay = true;
                audio.controls = 'controls';
                audio.src = _this.wavPath;
                audio.type = 'audioio/ogg';
                audio.style = 'display:none;';
                mwav.appendChild(audio);
            }

            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
}


// }
// function Message(arg) {
//     this.text = arg.text;
//     this.message_side = arg.message_side;

//     this.draw = function (_this) {
//         return function () {
//             let $message
//             if(_this.message_side == 'left') {
//                 $message = $($('.template_incoming').clone().html());
//                 $message.find('p.content').text(_this.text)
//             } else {
//                 $message = $($('.template_outgoing').clone().html());
//                 $message.find('p.content').text(_this.text)
//             }
//             $message.find('span.time_date').text(getTimeStamp());
//             $('.msg_history').append($message);
//             return setTimeout(function () {
//                 return $message.addClass('appeared');
//             }, 0);
//         };
//     }(this);
//     return this;
// }

// 톡봇 <--> Kochat 토글 스위치 함수
// function reset_talk(element) {
//     $('#msg_box').empty();

//     if(element.value == 'Kochat') {

//         answer_bot_id = '02927ec8-57aa-4d20-b468-b06c18dfa8df';
//         $.ajax({
//             url: 'http://49.50.161.221:8088/api/v1/chat/'+answer_bot_id+'/stopConversation/' + conv_id,
//             type: "GET",
//             success: function () {           
//                 userName = null;
//                 cur_bot = 'Kochat';
//                 sendMessage('안녕하세요. 아담한 토니입니다.', 'left');
//                 sendMessage('고객님의 성함을 입력해주세요.', 'left');
//                 console.log('Kochat으로 변환되었습니다.');
//             },
//             error: function (request, status, error) {
//                 return sendMessage('죄송합니다. 서버 연결에 실패했습니다.', 'left');
//             }
//         });
//     } else {
//         userName = null;
//         cur_bot = 'Talkbot';
//         text_flag = true;
//         greet();
//         console.log('Talkbot으로 변환되었습니다.');
//     }
// }

// 챗봇 열었을 때 안내 멘트를 시작하는 함수
function greet(talkBotId) {

    if (talkBotId == undefined) {
        talkBotId = "noTalkBotId"
    }

    if(text_flag === true) {
        $(() => {
            $(".chatbox-open").click(() => {
                $(".chatbox-popup, .chatbox-close").fadeIn()
            });
        });

        $.ajax({
            url: "/talkBot/",          
            type: "POST",
            data : JSON.stringify({'talkBotId' : talkBotId }),
            dataType: "json",
            contentType: 'application/json',
            success: function (data) {
                text_flag = false;
                setTimeout(function () {
                    return sendMessage(data.message, 'left', ['static/audio/login.wav']);
                });
            },
            error: function (request, status, error) {
                setTimeout(function () {
                    return sendMessage(['죄송합니다. 서버 연결에 실패했습니다.'], 'left');
                });
            }
        });
    }
    
};

function getMessageText() {
    let $message_input;
    let message = []
    $message_input = $('.message_input');
    message.push($message_input.val())
    return message
}

function sendMessage(messageArr, message_side, wavPath) {
    for(var i=0; i<messageArr.length; i++) {
        let $messages, message;
        $('.message_input').val('');
        $messages = $('.messages');
        if(!wavPath) { // wavPath가 존재하지않으면
            message = new Message({
                text: messageArr[i],
                message_side: message_side,
            });
        } else {    // wavPath가 존재하면
            message = new Message({
                text: messageArr[i],
                message_side: message_side,
                wavPath: wavPath[i],
            });
        }
        setTimeout(()=> message.draw(), 5000*i);
        $messages.animate({scrollTop: $messages.prop('scrollHeight')}, 300);
    }
}

// 메시지 입력 후 엔터 입력 시
function onClickAsEnter(e) {
   
    if (e.keyCode === 13) {
        onSendButtonClicked()
    }
}

// 메세지 입력(보내기 버튼 || 사용자 음성 인식)
function onClickAsClick(msg) {
    if(msg != null) {
        onSendButtonClicked()
    }
}



function requestTalkBot(messageText) {
    if (messageText[0].trim() == ''){
        setTimeout(function () {
            return sendMessage(['공백은 적절하지 못한 값입니다. 다시한번 입력해주세요.'], 'left');
        }, 1000);
    }
    
    $.ajax({
        url: '/talkBot/conv',
        type: "POST",
        data: JSON.stringify({'message' : messageText[0] }),
        dataType: "json",
        contentType: 'application/json',
        success: function (data) { 
            if(data.message.length == 0) {
                setTimeout(function () {
                    return sendMessage(['다시 입력해주세요.'], 'left');
                }, 1000);
            } else {
                setTimeout(() => {
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

function onSendButtonClicked() {
    let messageText = getMessageText();
    setTimeout(function () {
        sendMessage(messageText, 'right');
    }, 1000);
    $('.message_input').val('');
    return requestTalkBot(messageText);
}

function getTimeStamp() {
    var d = new Date();
    var s =
      leadingZeros(d.getFullYear(), 4) + '-' +
      leadingZeros(d.getMonth() + 1, 2) + '-' +
      leadingZeros(d.getDate(), 2) + ' ' +
  
      leadingZeros(d.getHours(), 2) + ':' +
      leadingZeros(d.getMinutes(), 2) + ':' +
      leadingZeros(d.getSeconds(), 2);
  
    return s;
}

function leadingZeros(n, digits) {
    var zero = '';
    n = n.toString();

    if (n.length < digits) {
        for (i = 0; i < digits - n.length; i++)
        zero += '0';
    }
    return zero + n;
}