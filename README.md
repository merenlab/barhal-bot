This is a very simple bot to keep an eye on an our SGE instance (for now).

## How to setup the right environment

``` bash
# create a Python virtual environment anywhere you like:
virtualenv /groups/merenlab/virtual-envs/barhalbot/

# activate it:
source /groups/merenlab/virtual-envs/barhalbot/bin/activate

# install slackclient for python:
pip install slackclient

# add an alias to activate it:
echo 'alias barhal-bot-activate="source /groups/merenlab/virtual-envs/barhalbot/bin/activate"' >> ~/.bash_profile
source ~/.bash_profile

# get a copy of the repository
cd /groups/merenlab/github/
git clone https://github.com/merenlab/barhal-bot.git
```


## How to run

``` bash
# activate the bot and get into the source code dir
barhal-bot-activate
cd /groups/merenlab/github/

# run it
export SLACK_BOT_TOKEN='SLACK TOKEN HERE'
./bot
```

If you get an certificate error, it is due to a bug upstream. In which case you can download this file once:

```
wget https://www.tbs-certificats.com/issuerdata/DigiCertGlobalRootCA.crt
```

And you can export the following environmental variable before you run it:

```
export WEBSOCKET_CLIENT_CA_BUNDLE=DigiCertGlobalRootCA.crt
```

## How to test

When the `--test-command` parameter is given, the bot will not try to connect to Slack and will simply run the command and return the response to the terminal:

```
./bot --test-command test
./bot --test-command queue
./bot --test-command queue user oesen
```

## Thanks

The very initial version of this bot was inspired from the [tutorial](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html) by Matt Makai.
