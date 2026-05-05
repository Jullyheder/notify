import os
import requests


class CallMeBot:

    def __init__(self):
        self.__base_url = os.getenv('CALLMEBOT_API_URL')
        self.__phone_number = os.getenv('CALLMEBOT_PHONE_NUMBER')
        self.__api_key = os.getenv('CALLMEBOT_API_KEY')

    def send_message(self, message: str):
        response = requests.get(
            url=f'{self.__base_url}?phone={self.__phone_number}&text={message}&apikey={self.__api_key}'
        )
        return response.text
