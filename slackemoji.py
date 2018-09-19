from slackclient import SlackClient
import re
import csv


class SlackEmoji():

    def __init__(self, token, call_limit):
        self.token = token
        self.call_limit = call_limit
        self.slackclient = SlackClient(token)
        self.emoji_pattern = re.compile(":([a-z0-9_\+\-]+):")
        self.found_emojis = dict()

    def paginated_api_call(self, method, response_objects_name, **kwargs):
        ret = list()
        cursor = None
        while cursor != "":
            r = self.slackclient.api_call(method, limit=self.call_limit, cursor=cursor, **kwargs)
            if response_objects_name in r:
                ret.extend(r[response_objects_name])

            if "response_metadata" in r:
                cursor = r["response_metadata"]["next_cursor"]
            else:
                cursor = ""

        return ret;

    def get_channels(self):
        return self.paginated_api_call("conversations.list",
                                       "channels",
                                       exclude_archived=True,
                                       types="public_channel"
                                       )

    def get_messages(self, channel_id):
        return self.paginated_api_call("conversations.history",
                                       "messages",
                                       channel=channel_id
                                       )

    def get_replies(self, channel_id, ts):
        return self.paginated_api_call("conversations.replies",
                                       "messages",
                                       channel=channel_id,
                                       ts=ts
                                       )

    def parse(self):
        for channel in self.get_channels():
            self.parse_messages_in_channel(channel["id"])

    def parse_messages_in_channel(self, channel_id):
        for message in self.get_messages(channel_id):
            if "subtype" not in message:
                self.parse_message(message["text"])

                if "reactions" in message:
                    self.parse_reactions(message["reactions"])

                if "reply_count" in message and message["reply_count"] > 0:
                    self.parse_reply_to_message(channel_id, message["ts"])

    def parse_reply_to_message(self, channel_id, message_id):
        for reply in self.get_replies(channel_id, message_id):
            if "reply_count" not in reply:
                self.parse_message(reply["text"])

                if "reactions" in reply:
                    self.parse_reactions(reply["reactions"])

    def parse_reactions(self, reactions):
        for reaction in reactions:
            self.add_emoji_to_list(reaction["name"], reaction["count"])

    def parse_message(self, message):
        for m in self.emoji_pattern.finditer(message):
            self.add_emoji_to_list(m.group(1))

    def add_emoji_to_list(self, emoji, count=1):
        if "::" in emoji:
            emoji = emoji[0: emoji.find("::")]

        if emoji in self.found_emojis:
            self.found_emojis[emoji] += count
        else:
            self.found_emojis[emoji] = count

    def print_list(self):
        for emoji in sorted(self.found_emojis):
            print(emoji + "," + str(self.found_emojis[emoji]))

    def save_to_file(self, filename):
        with open(filename, 'w', newline='') as f:
            w = csv.writer(f, dialect='excel')
            w.writerows(self.found_emojis.items())