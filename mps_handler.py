import os
import requests
import time    

class MPSHandler:
    def __init__(self, env_var_name="MATHPIXSNIP_KEY"):
        self.api_key = os.environ.get(env_var_name)
        self.app_id = 'teamhammerspace_gmail_com_151e1c_ee0faa'
        self.tmp_key = ''
        self.tmp_key_expr = 0
        self.TOKEN_ENDPOINT = 'https://api.mathpix.com/v3/app-tokens'
        self.TRANSLATE_ENDPOINT = "https://api.mathpix.com/v3/text"
        self.TRANSLATE_PDF_ENDPOINT = "https://api.mathpix.com/v3/pdf"
    
    def __loadTemporaryToken(self):
        
        epoch_time = int(time.time())
        if epoch_time - self.tmp_key_expr > 45:
            return

        headers = {
            "app_key": self.api_key,
            "app_id": self.app_id
        }
        response = requests.post(self.TOKEN_ENDPOINT, headers=headers)
        self.tmp_key = response['app_token']
        self.tmp_key_expr = response['app_token_expires_at']
    
    def __generatePayload(self, img_url):
        payload = {
            "src": img_url,
            "formats": ["text"],
            "math_inline_delimiters": ["$", "$"],
            "math_display_delimiters": ["$$", "$$"],
            "format_options": {
                "text": {
                    "transforms": ["rm_spaces", "rm_newlines"]
                }
            }
        }
        headers = {
            'Content-type': 'application/json',
            'app_id': self.app_id,
            'app_key': self.api_key
        }
        return (headers, payload)
    
    def postprocess(self, t: str) -> str:
        return ' '.join(t.replace('\\\\', '\\').split('\n'))

    def GetTranslation(self, img_url):
        self.__loadTemporaryToken()
        headers, payload = self.__generatePayload(img_url)
        response = requests.post(self.TRANSLATE_ENDPOINT, json=payload, headers=headers)
        print("api key", self.api_key)
        print("response is", response)
        print("response json is", response.json())
        json = response.json()
        if 'text' in json:
            return self.postprocess(response.json()['text'])
        else:
            return response.json()
        
        


    

    