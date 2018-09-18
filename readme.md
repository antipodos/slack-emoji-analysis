Slack Emoji Analysis
=

Parses slack messages in all public channels and compiles a list of all emojis used in
- messages
- replies to messages
- reactions to messages
- reactions to replies

Counters will be printed to command line or additionally saved to a csv file.

Preparation
-

[Create an app](https://api.slack.com/apps) in your slack workspace. The app needs the following permission scopes:
- `channels:read`
- `channels:history`

Get the app's `OAuth Access Token` from the app's management page.
To get the provided example running register the token as an environment variable called `SLACK_TOKEN`.
  
Usage
-

You can simply run the `example.py` file in any python 3.6+ environment. If you want the result as a csv file just pass in the filename (if existing it will be overwritten!) as the only parameter:

`python path/to/example.py path/to/emojis.csv` 