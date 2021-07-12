import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import requests
import json
from random import randint
from typing import Dict, Union, NoReturn  ## typing : 타입 표시

class CTalkBot:
    def __init__(self, bot_id: str = None) -> None:
        if bot_id is None :
            bot_id = "02927ec8-57aa-4d20-b468-b06c18dfa8df"
        self.answer_bot_id = bot_id  ## talkbot id


    def start_conversation(self, bot_id : str = None) -> Union[str, None]:  ## String일 수도 None일 수도

        if bot_id is None:
            bot_id = self.answer_bot_id
        
        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/startConversation'.format(self.answer_bot_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        bot_response = self.do_get(url=api_url, params=None, headers=headers)

        if bot_response is None:
            return None

        else:
            self.conv_id = bot_response['conversationId']
            return bot_response['conversationId'], bot_response


    def conversation(self, query: str = None, bot_id: str = None, conv_id: str = None) -> Dict:

        if bot_id is None :
            bot_id = self.answer_bot_id
        
        if conv_id is None :
            conv_id = self.conv_id
        
        if query is None :
            query = ""

        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/{}/1'.format(self.answer_bot_id, self.conv_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        bot_response = self.do_post(url=api_url, body=query.encode('utf-8'), headers=headers)
        
        if bot_response is None:
            return None

        else:
            return bot_response


    def stop_conversation(self, bot_id: str = None, conv_id: str = None) -> NoReturn:  

        if bot_id is None :
            bot_id = self.answer_bot_id
        
        if conv_id is None :
            conv_id = self.conv_id

        api_url = 'http://49.50.161.221:8088/api/v1/chat/{}/stopConversation/{}'.format(self.answer_bot_id, self.conv_id)
        headers = {'User-Agent': 'Mozila/5.0', 'Content-type': 'application/json'}
        requests.get(api_url, headers=headers, params=None)


    def do_post(self, url: str, body: str, headers: Dict = None) -> Union[Dict, None]:
        response = requests.post(url, headers=headers, data=body)

        status_code = response.status_code
        if status_code != 200:
            response.raise_for_status()
            return None

        return response.json()


    def do_get(self, url: str, params: Dict, headers: Dict = None) -> Union[Dict, None]:
        response = requests.get(url, headers=headers, params=params)

        status_code = response.status_code

        if status_code != 200:
            response.raise_for_status()
            return None

        return response.json()
