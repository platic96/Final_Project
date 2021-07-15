import pprint
import os
import jwt
import uuid
import hashlib
import requests
from urllib.parse import urlencode

import requests

class coin:

    loginData = [
        {"secretkey":"GW01NgJHYxx8VRRE4oVb5xcpm5rDcENJyEqKHsie", "accesskey":"Kjd7XuRjnwmHHMmaMHDjzNjUTjqwpFjHtw0C8Wjd", "name":"김민재"},
        {"secretkey":"GW01NgJHYxx8VRRE4oVb5xcpm5rDcENJyEqKHsie", "accesskey":"Kjd7XuRjnwmHHMmaMHDjzNjUTjqwpFjHtw0C8Wjd", "name":"허윤석"}
    ] 
    

    def __init__(self, ID: str):

        for i in range(len(self.loginData)) :
            if self.loginData[i]['name'] == ID :
                self.access_key = self.loginData[i]['accesskey']
                self.secret_key = self.loginData[i]['secretkey']
            else :
                self.message = '없는 아이디 입니다.'


        self.server_url = 'https://api.upbit.com'
        
        self.payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }

    def maker_headers(self) -> dict:
        jwt_token = jwt.encode(self.payload, self.secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        return headers

    # 보유중인 코인의 간단한 정보를 가져온다.
    # 평균 매수가는 가져오나 현재 거래가격을 가져오지 않아 다른작업을 해줘야한다.
    def account(self) -> list:
        maker_headers = self.maker_headers()
        res = requests.get(self.server_url + "/v1/accounts", headers=maker_headers)
        return res.json()

    # 투자현황에 대한 멘트를 만들어 준다. 현재 투자한 가격정보를 직접 만들어 주어야한다.
    def investment_status(self) -> str:
        # 현재 거래 정보를 가져온다.
        trade_infos, account_list= self.ticker_trade_infos(self.account(), "account")

        
        # 멘트를 만들어준다.
        ment = "현재 {}개의 코인에 투자 중입니다. 현재가치로는 ".format(len(trade_infos))
        for trade_info, account_coin in zip(trade_infos, account_list[1:]):
            ment += "{} : {}원, ".format(account_coin['currency'],
            int(float(account_coin['balance']) * float(trade_info['trade_price'])))

        return ment

    # 자산현황에 대한 멘트를 만들어 준다.
    def asset_status(self) -> str:
        # 현재 거래 정보를 가져온다.
        trade_infos, account_list= self.ticker_trade_infos(self.account(), "account")
        ment = "현재 투자 코인의 자산으로는 "
        
        for trade_info, account_coin in zip(trade_infos, account_list[1:]):
            ment += "{} : {}%, ".format(account_coin['currency'], 
            round(float(trade_info['trade_price'])/(float(account_coin['avg_buy_price']))* 100, 2))

        return ment
    
    def coin_status(self, top: int) -> str:
        # 현재 코인리스트 정보를 가져온다.
        trade_infos, account_list= self.ticker_trade_infos(self.all_market(), 'all')
        trade_infos = sorted(trade_infos, key = (lambda x: x['acc_trade_price_24h']))
        
        ment = '현재 거래량 상위 3개 현황입니다. '
        for trade_info in reversed(trade_infos[-top:]):
            ment += '{} : {}원 전일대비 {}%, '.format(
                trade_info['market'], round(trade_info['trade_price']),
                round(trade_info['trade_price'] /trade_info['prev_closing_price'] * 100, 2))
        return ment


    # 현재 코인의 거래가격을 가져와야한다 . 그래야 자신이 가지고있는 재산정보를 확인할 수 있다.
    def ticker_trade_infos(self, account_list: list, account='account') -> list:
        # 자신의 코인들을 가져온다.
        # account_list = self.account()

        coin_list = []
        # markets에 넣어줄값을 만들어준다. list형식으로
        
        # account는 내가 소유중인 화폐만, all은 전체
        if account == 'account':
            for coin in account_list[1:]:
                coin_list.append(coin['unit_currency'] + '-' + coin['currency'])
        elif account == 'all':
            for coin in account_list:
                coin_list.append(coin['market'])
		
        if 'KRW-APENFT' in coin_list :
            coin_list.remove('KRW-APENFT')
			
        url = "https://api.upbit.com/v1/ticker"
        querystring = {"markets":" KRW-BTT",
                   "markets": ','.join(coin_list)}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        return response, account_list
        
    # 모든 암호화폐의 영문명 한글명을 가져온다.
    def all_market(self) -> list:
        
        url = "https://api.upbit.com/v1/market/all"
        querystring = {"isDetails":"false"}
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()

def main(argument):
  
  key =  coin(argument['ID'])

  if argument['flag'] == '코인':
    return {'result' : key.coin_status(5) }
  elif argument['flag'] == '투자':
    return {'result' : key.investment_status() }
  elif argument['flag'] == '자산':
    return {'result' : key.asset_status() }


# key = coin('허윤석')
# print(key.asset_status())
#print(key.coin_status(5))
# print(key.investment_status())
# print(key.all_market()[0])
# print(key.ticker_trade_infos(key.all_market(), 'all'))
  