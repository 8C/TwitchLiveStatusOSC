import config
import time
import requests
import platform
import urllib.request
import os
from pythonosc.udp_client import SimpleUDPClient

IP, PORT = "127.0.0.1", 9000
client = SimpleUDPClient(IP, PORT) 
announced = False
buffer = 5 * 60 #5min

request_token_url = f"https://id.twitch.tv/oauth2/token?client_id={config.twitch_api_key}&client_secret={config.twitch_api_secret}&grant_type=client_credentials"
reponse = requests.post(request_token_url)
print(reponse)
token = reponse.json()['access_token']
header = {'Client-ID': config.twitch_api_key, "Authorization": f'Bearer {token}'}

cls = "cls" if platform.system() == "Windows" else "clear"


def getThumbnail(url):
    folder_path = "./thumbnail/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    file_name = 'thumbnail.jpg'

    #if thumbnail already exists, delete it
    if os.path.exists(os.path.join(folder_path, file_name)):
        os.remove(os.path.join(folder_path, file_name))


    local_file = os.path.join(folder_path, file_name)
    urllib.request.urlretrieve(url, local_file)


if __name__ == '__main__':
   
    while True:
        os.system(cls)
        print(f'Checking if {config.twitch_username} is live on twitch...')
        response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={config.twitch_username}', headers=header)
        if response.status_code == 200:
            data = response.json()["data"]
            if data:
                broadcaster = data[0]
                broadcaster_id = broadcaster["id"]
                broadcaster_name = broadcaster["user_name"]
                broadcaster_game = broadcaster["game_name"]
                stream_title = broadcaster["title"]


                if not announced:
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', True)
                    print("user is live on twitch!")
                    announced = True
                    time.sleep(buffer)
                else:
                    time.sleep(buffer)
            else:
                if announced:
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', False)
                    print("user is no longer live on twitch")
                    announced = False
                    time.sleep(buffer)
                else:
                    print("user is not live on twitch right now")
                    client.send_message(f'/avatar/parameters/{config.vrc_param}', False)
                    announced = False
                    time.sleep(buffer)
        else:
            print('Error: ' + str(response.status_code) + ' ' + response.text)
            

