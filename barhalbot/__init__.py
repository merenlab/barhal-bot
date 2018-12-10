import re
import os
import sys
import time

from slackclient import SlackClient

from barhalbot.commands import simple_commands, complex_commands


class Bot:
    def __init__(self, args):
        A = lambda x: args.__dict__[x] if x in args.__dict__ else None
        self.test_command = A('test_command')

        self.command = None
        self.channel = None

        if self.test_command:
            self.handle_command(args.test_command)
            sys.exit()

        try:
            token = os.environ.get('SLACK_BOT_TOKEN') if not os.path.exists('SLACK_BOT_TOKEN') else open('SLACK_BOT_TOKEN').readline().strip()
        except:
            print("Either set SLACK_BOT_TOKEN environment variable, or create a file with the AUTH names 'SLACK_BOT_TOKEN' :/")
            sys.exit()


        # big deal line:
        self.slack_client = SlackClient(token)

        if self.slack_client.rtm_connect(with_team_state=False):
            print("Up and listening :)")

            # Read bot's user ID by calling Web API method `auth.test`
            self.bot_name = self.slack_client.api_call("auth.test")["user_id"]

            while True:
                self.command, self.channel = self.read_slack(self.slack_client.rtm_read())

                if self.command:
                    self.handle_command(self.command)

                time.sleep(1)
        else:
            print("Connection failed. Exception traceback printed above.")


    def read_slack(self, slack_events):
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.bot_name:
                    return message, event["channel"]

        return None, None


    def parse_direct_mention(self, message_text):
        matches = re.search("^<@(|[WU].+?)>(.*)", message_text)

        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


    def respond(self, response):
        print("- Response ..: ", response)
        print()

        if self.channel:
            self.slack_client.api_call("chat.postMessage",
                                       channel=self.channel,
                                       text=response)


    def handle_command(self, command):
        print("- Command ...: ", command)

        if command in simple_commands:
            self.respond(simple_commands[command])
        elif command.split()[0] in complex_commands:
            self.respond(complex_commands[command.split()[0]](command))
        else:
            self.respond("I am not a very smart bot :( I know these commands: %s." % (', '.join(complex_commands.keys())))
