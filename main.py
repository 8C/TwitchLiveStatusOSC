import config
import time
import requests
import platform
import os
from pythonosc.udp_client import SimpleUDPClient

IP, PORT = "127.0.0.1", 9000
client = SimpleUDPClient(IP, PORT) 
announced = False
buffer = 5 * 60 #5min delay

request_token_url = f"https://id.twitch.tv/oauth2/token?client_id={config.twitch_api_key}&client_secret={config.twitch_api_secret}&grant_type=client_credentials"
reponse = requests.post(request_token_url)
print(reponse)
token = reponse.json()['access_token']
header = {'Client-ID': config.twitch_api_key, "Authorization": f'Bearer {token}'}
cls = "cls" if platform.system() == "Windows" else "clear"


if __name__ == '__main__':
   
    while True:
        os.system(cls)
        print(f'Checking if {config.twitch_username} is live on twitch...')
        response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={config.twitch_username}', headers=header)
        if response.status_code == 200:
            data = response.json()["data"] #lazy rn
            if data:
                if not announced:
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', True)
                    print("User is live on twitch")
                    announced = True
                    time.sleep(buffer)
                else:
                    time.sleep(buffer)
            else:
                if announced:
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', False)
                    print("User is no longer live on twitch")
                    announced = False
                    time.sleep(buffer)
                else:
                    print("User is not live on twitch right now")
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', False)
                    announced = False
                    time.sleep(buffer)
        else:
            print('Error: ' + str(response.status_code) + ' ' + response.text)
            

