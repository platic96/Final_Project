import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import requests
import json
from random import randint
from typing import Dict, Union, NoReturn  ## typing : 타입 표시
from Global import Global_veriable
import pprint

class CTalkBot:
    def __init__(self,bot_id: str) -> None:
        self.bot_id = bot_id
        self.conv_id, start_message = self.start_conversation()

    def call_talkbot(self,query: str) -> None:
         ## 톡봇과의 대화 연결

        if query != '종료':
            answer = self.conversation(query=query)  ## 톡봇에게 응답 넘기고, 응답 받기
        elif query == '종료':
            self.stop_conversation()  ## 톡봇과 연결 종료
        return answer


    def start_conversation(self) -> Union[str, None]:  ## String일 수도 None일 수도
        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/startConversation'.format(self.bot_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        bot_response = self.do_get(url=api_url, params=None, headers=headers)
        print(bot_response)

        if bot_response is None:
            return None

        else:
            return bot_response['conversationId'], bot_response


    def conversation(self, query: str) -> Dict:
        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/{}/1'.format(self.bot_id, self.conv_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        bot_response = self.do_post(url=api_url, body=query.encode('utf-8'), headers=headers)
        
        if bot_response is None:
            return None

        else:
            return bot_response


    def stop_conversation(self) -> NoReturn:  
        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/stopConversation/{}'.format(self.bot_id, self.conv_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        requests.get(api_url, headers=headers, params=None)


    def do_post(self,url: str, body: str, headers: Dict = None) -> Union[Dict, None]:
        response = requests.post(url, headers=headers, data=body)

        status_code = response.status_code
        if status_code != 200:
            response.raise_for_status()
            return None

        return response.json()


    def do_get(self,url: str, params: Dict, headers: Dict = None) -> Union[Dict, None]:
        response = requests.get(url, headers=headers, params=params)

        status_code = response.status_code

        if status_code != 200:
            response.raise_for_status()
            return None

        return response.json()


    # def init(self):
    #     # answer_bot_id = '0061b0fd-0eea-47a7-b886-34213967ccb5'  ## talkbot id
    #     call_talkbot(bot_id=answer_bot_id)  ## coversation id

# if __name__=="__main__":
#     main()