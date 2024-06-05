"""
The main file of the bot, i have no idea what i'm doing

TO DO:

-clean up documentation and HTTP requests since they aren't readable at all
-mysql/sqlite integration (probably both)
-error handling?
-bot should probably be able to work on many streams at once and that's not the case for now
"""
from commands import Command
import requests as rq
import json
import authconfig
import threading
import websocket as ws
ws.enableTrace(True)

def get_user_id(user: str) -> str:
    """
    Gets twitch user ID as a string
    :param user: (str) a twitch username that you want to know the ID of
    :return: (str) user ID
    """
    userurl = 'https://api.twitch.tv/helix/users?login={}'.format(user)
    userdata = rq.get(userurl, headers={'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}).text
    return json.loads(userdata)['data'][0]['id']

def send_message(channel: str, message: str):
    """
    Sends a message to a twitch channel's chat
    :param channel: the channel name you wish to send a message to
    :param message: the message you wish to send
    :return: None
    """
    rq.post('https://api.twitch.tv/helix/chat/messages',
                  headers={ 'Client-Id': authconfig.client_id,
                            'Authorization': 'Bearer {}'.format(authconfig.user_token),
                            'Content-type': 'application/json'},
                  data=json.dumps({
                        'broadcaster_id': '{}'.format(get_user_id(channel)),
                        'sender_id': '{}'.format(get_user_id(authconfig.username)),
                        'message': '{}'.format(message)}))


def _onmessage(wsapp, message) -> None:
    """
    Function reacts to websocket messages that occur during connection.
    :param wsapp: (object) the websocket connection that the messages are coming from
    :param message: (object) The websocket message
    :return:
    """
    if json.loads(message)['metadata']['message_type'] == 'notification':
        print(json.loads(message)['payload']['event']['badges'])
        chat_message = json.loads(message)['payload']['event']['message']['text']
        print(chat_message)
        if chat_message.startswith("!"):
            mod = False
            for i in json.loads(message)['payload']['event']['badges']:
                if i.get('set_id') == 'moderator' or i.get('set_id') == 'broadcaster':
                    mod = True
                    break
            if Command.commands.get(chat_message.split()[0][1:]):
                send_message(authconfig.channel, Command.commands[chat_message.split()[0][1:]](mod, chat_message))
            else:
                send_message(authconfig.channel, "Command {} not found.".format(chat_message.split()[0]))

    if json.loads(message)['metadata']['message_type'] == 'session_welcome':
        sessionid = json.loads(message)['payload']['session']['id']
        dataforrequest = json.dumps({
            'type': 'channel.chat.message',
            'version': '1',
            "condition": {
                "broadcaster_user_id": get_user_id(authconfig.channel),
                "user_id": get_user_id(authconfig.username)},
            'transport': {
                "method": "websocket",
                "session_id": sessionid}})

        rq.post('https://api.twitch.tv/helix/eventsub/subscriptions',
                    headers={'Client-Id': authconfig.client_id,
                             'Authorization': 'Bearer {}'.format(authconfig.user_token),
                             'Content-type': 'application/json'}, data=dataforrequest)

        send_message(authconfig.channel, "AutoKozak is here!")



authheaders = {'Client-Id': authconfig.client_id, 'Authorization': 'Bearer {}'.format(authconfig.app_token)}
socket = ws.WebSocketApp("wss://eventsub.wss.twitch.tv/ws", header=authheaders, on_message=_onmessage)
socket.run_forever(sslopt={'username':authconfig.username,
                           'password':'oauth:{}'.format(authconfig.app_token),
                           'channels':authconfig.channel})








