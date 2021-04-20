#!/usr/bin/python3

import discord

import time
import datetime
import json
import sys
import argparse
from pathlib import Path

class MyClient(discord.Client):
    def __init__(self, log_loc, twit):
        self.log_loc = Path(log_loc)
        if not self.log_loc.exists():
            self.log_loc.touch()
            with open(self.log_loc, "w") as f:
                f.write(header+"\n")
        super().__init__()

    async def on_ready(self):
        print('Logged on as',self.user)
        print(self.guilds)

    async def on_message(self,message):
        # print("message:",message)
        pass

    async def on_disconnect(self):
        #api.PostDirectMessage("Client disconnected", twitter_id)
        pass

    async def on_connect(self):
        if twit:
            api.PostDirectMessage("Client Connected", twitter_id)


    async def on_voice_state_update(self, member, before, after):
        if str(member.guild.id) == discord_guild_id:
            member_name = str(member)
            guild_name = str(member.guild)
            if before.channel == after.channel: #mute/deaf
                channel_name = str(before.channel.name)
                state = "unknown"
                if before.self_mute != after.self_mute: #mute changed
                    # print("Muted: "+str(after.self_mute))
                    if after.self_mute:
                        state = "muted"
                    elif not after.self_mute:
                        state = "unmuted"
                elif before.self_deaf != after.self_deaf:
                    # print("Deafened: "+str(after.self_deaf))
                    if after.self_deaf:
                        state = "deafened"
                    elif not after.self_deaf:
                        state = "undeafened"
                elif before.self_stream != after.self_stream:
                    # print("Streaming: "+str(after.self_stream))
                    if after.self_stream:
                        state= "streaming"
                    elif not after.self_stream:
                        state = "not streaming"
                output = ",".join([timestamp(), member_name,guild_name, channel_name, state])
                print(output)
                saveOutput(output, self.log_loc)
                return
            if after.channel == None: #leaving
                channel_name = str(before.channel.name)
                message = member_name+" left "+guild_name+" Voice Channel "+channel_name
                output = ",".join([timestamp(), member_name,guild_name, channel_name, "leave"])
                saveOutput(output, self.log_loc)
                print(message)
                if twit:
                    api.PostDirectMessage(message, twitter_id)
            if not after.channel == None: #join from nothing
                channel_name = str(after.channel.name)
                message = member_name+" joined "+guild_name+" Voice Channel "+channel_name
                output = ",".join([timestamp(), member_name,guild_name, channel_name, "join"])
                saveOutput(output, self.log_loc)
                print(message)
                if twit:
                    api.PostDirectMessage(message, twitter_id)

def saveOutput(message, log):
    with open(log, 'a+') as f:
        f.write(message+"\n")

def timestamp():
    tim = datetime.datetime.now()
    return "/".join([str(tim.day),str(tim.month),str(tim.year)])+" "+":".join([str(tim.hour),str(tim.minute),str(tim.second)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discord Voice notification bot")

    parser.add_argument('-c', '--config', dest="config", action="store", default="private.json", help="Config file location")
    parser.add_argument('-t', '--twitter', dest="twitter", action="store_true", default=False, help="Twitter DMs")
    parser.add_argument('-l', '--log', dest="log", action="store", default="voice.log", help="Log Location")
    parser.add_argument('-b', '--bot', dest="bot", action="store_true", default=False, help="Login in as bot")
    parser.add_argument('--header', dest="header", action="store_true", default=False, help="Output header")

    args = parser.parse_args()

    header = "timestamp, user, guild, channel, state"

    if args.header:
        print(header)

    with open(args.config, 'r') as f:
        data = json.loads(f.read())
        try:
            discord_token = data['discord_token']
            discord_guild_id = data['discord_guild_id']
            twit = False
            if args.twitter:
                import twitter
                api_key = data['api_key']
                api_secret_key = data['api_secret_key']
                access_token = data['access_token']
                access_token_secret = data['access_token_secret']
                twitter_id = data['twitter_id']
                api = twitter.Api(consumer_key=api_key,
                                consumer_secret=api_secret_key,
                                access_token_key=access_token,
                                access_token_secret=access_token_secret)
                twit = True
        except KeyError:
            sys.exit("Error reading config file")

    client = MyClient(args.log, twit)
    try:
        client.run(discord_token, bot=args.bot)
    except LoginFailure:
        if twit:
            api.PostDirectMessage("Bad login", twitter_id)
        else:
            print("Login failure!!!")



