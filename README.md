# discordvoicemon

Monitor a server's voice channels and log all of the activity (not the sound the activity like people leaving, joining, muting, deafening, streaming)

## Requirements
Depends on [`discord`](https://pypi.org/project/discord.py/) python library, in addition to the [`twitter`](https://pypi.org/project/twitter/) python library,along with appropriate api and token keys.

You can install these with pip;
- `pip install discord.py`
- `pip install twitter`

Everything else is from default python libraries.

If you are running this on a user profile be aware that this is against discord's TOS and may end with your account being banned. If you are using a bot, make sure that you use the `-b`/`--bot` flag.


## Simple Usage

`python3 discordvs.py`

Will open the json config (`private.json`) file in the same directory, connect to discord and begin logging output to default log file, `voice.log` it the same folder.

## Advanced Usage

You can also configure the script to send push notifications to a twitter DM using the `-t` flag. This will make the script check the config file for:
- `api_key`: twitter api key
- `api_secret_key`: twitter secret key
- `access_token`: twitter account access token
- `access_token_secret`: twitter account access token secret
- `twitter_id`: twitter user id to send messages to
