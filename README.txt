This is going to be my first attempt to build a Twitch channel bot with Python and learn Git in the meantime

Removing authconfig.py from the repo because I will definitely leak things that should not be leaked.
If anyone ever tries to run it, you need an authconfig file with these things defined:

username = {your bot's twitch username}
client_id = {client id of your app from https://dev.twitch.tv/console/apps}
app_token = {app token for your app. https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/}
user_token = {token from your bot's twitch account. I will upload necessary scopes shortly (probably like 3 months lol). instructions for obtaining at https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/  ( i like implicit grant flow)
secret = {secret/password of your app from https://dev.twitch.tv/console/apps}

