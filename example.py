from slackemoji import SlackEmoji
import os
import sys

token = os.environ["SLACK_TOKEN"]
call_limit = 1000

se = SlackEmoji(token, call_limit)
se.parse()
se.print_list()

if len(sys.argv) == 2 and \
        os.path.isdir(os.path.dirname(sys.argv[1])):
    se.save_to_file(sys.argv[1])