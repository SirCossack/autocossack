import requests as rq
import websocket as ws
import json
import authconfig

def get_user_id(user):
    userurl = 'https://api.twitch.tv/helix/users?login={}'.format(user)
    userdata = rq.get(userurl, headers={'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}).text
    return json.loads(userdata)['data'][0]['id']

ws.enableTrace(True)

authheaders = {'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}
socket = ws.WebSocket(sslopt={'username':authconfig.username, 'password':'oauth:{}'.format(authconfig.app_token),'channels':authconfig.username})
socket.connect("wss://eventsub.wss.twitch.tv/ws")
sessionid = json.loads(socket.recv())['payload']['session']['id']
print(sessionid)


dataforrequest = json.dumps({
    'type': 'channel.chat.message',
    'version': '1',
    "condition": {
        "broadcaster_user_id": get_user_id(authconfig.username),
        "user_id": get_user_id(authconfig.username)},
    'transport': {
        "method": "websocket",
        "session_id": sessionid}
})
print(dataforrequest)

a = rq.post('https://api.twitch.tv/helix/eventsub/subscriptions', headers={'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.user_token), 'Content-type': 'application/json'}, data=dataforrequest)
print(a.text)
print(socket.recv())





