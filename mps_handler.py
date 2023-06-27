import os
import requests

class MPSHandler:
    def __init__(self, env_var_name="MATHPIXSNIP_KEY", endpoint=):
        self.api_key = os.environ.get(env_var_name)
        self.tmp_key = ''
        self.tmp_key_expr = 0
        self.TOKEN_ENDPOINT = 'https://api.mathpix.com/v3/app-tokens'
        self.TRANSLATE_ENDPOINT = "https://api.mathpix.com/v3/text"
    
    def __loadTemporaryToken(self):
        headers = {
            "app_key": self.api_key
        }
        response = requests.post(self.TOKEN_ENDPOINT, headers=headers)
        self.tmp_key = response['app_token']
        self.tmp_key_expr = response['app_token_expires_at']
    
    def __generatePayload(self, img_url):
        payload = {
            "src": url,
            "formats": ["text", "data"],
            "data_options": {
                "include_asciimath": true
            }
        }
        headers = {'content-type': 'application/json'}
        return (headers, payload)

    def GetTranslation(self, img_url):
        self.__loadTemporaryToken()
        headers, payload = self.__generatePayload(img_url)
        response = requests.post(self.TRANSLATE_ENDPOINT, json=payload, headers=headers)
        return response['text']
        


    

    