"""
The main file of the bot, i have no idea what i'm doing

TO DO:

-clean up documentation and HTTP requests since they aren't readable at all
-get a bot to post something (need a new token, don't know what access scopes i'll need yet but i'll probably need to get a new one like 5-10 times during development)
-set up actual commands

in the far future
- error handling
- mysql/sqlite integration (probably both)
-
"""
import commands
import requests
import requests as rq
import websocket as ws
import json
import authconfig

def get_user_id(user: str) -> str:
    """
    Gets twitch user ID as a string
    :param user: (str) a twitch username that you want to know the ID of
    :return: (str) user ID
    """
    userurl = 'https://api.twitch.tv/helix/users?login={}'.format(user)
    userdata = rq.get(userurl, headers={'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}).text
    return json.loads(userdata)['data'][0]['id']
def _onmessage(wsapp, message):
    """
    Function reacts to websocket messages that occur during connection.
    :param wsapp: (object) the websocket connection that the messages are coming from
    :param message: (object) The websocket message
    :return:
    """
    if json.loads(message)['metadata']['message_type'] == 'notification':

        if json.loads(message)['payload']['event']['message']['text'].startswith('!counter'):
             print(rq.post('https://api.twitch.tv/helix/chat/messages',headers={'Client-Id': authconfig.client_id,
                              'Authorization': 'Bearer {}'.format(authconfig.user_token),
                              'Content-type': 'application/json'}, data=json.dumps({
                 'broadcaster_id': '{}'.format(get_user_id(authconfig.username)),
                 'sender_id': '{}'.format(get_user_id(authconfig.username)),
                 'message': '{}'.format(commands.counter())
             })))

    if json.loads(message)['metadata']['message_type'] == 'session_keepalive':
        return
    if json.loads(message)['metadata']['message_type'] == 'session_welcome':
        sessionid = json.loads(message)['payload']['session']['id']
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
        a = rq.post('https://api.twitch.tv/helix/eventsub/subscriptions',
                    headers={'Client-Id': authconfig.client_id,
                             'Authorization': 'Bearer {}'.format(authconfig.user_token),
                             'Content-type': 'application/json'}, data=dataforrequest)
        print(a)
    print(json.loads(message))



requests.Response

ws.enableTrace(True)

authheaders = {'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}
socket = ws.WebSocketApp("wss://eventsub.wss.twitch.tv/ws", header=authheaders, on_message=_onmessage)

sc = socket.run_forever(sslopt={'username':authconfig.username, 'password':'oauth:{}'.format(authconfig.app_token),'channels':authconfig.username})








