# Dbot - Discord command bot
A small modular discord micro-bot written in Python.

Originally it was a bot made for a private community so the original code may
be a few years old but I've updated it for Python3.6 (Discord dosen't yet 
support 3.7 yet as of writing this). It's a stripped down skeleton of what it
originally once was so it's a easy to get up and running and then expand with
new extensions depending on what it will be used for.


## TLDR (Python 3.6.x)
```sh
pip install -r requrements.txt
./main.py
```

## Ubuntu 18.04.1 LTS (Python 3.6.5)
```sh
# Download it and go into folder
git clone https://gitlab.com/renegadevi/dbot.git
cd dbot

# Optional: Virtualenv
apt install git virtualenv
virtualenv -p python3 venv
source venv/bin/activate

# Install required modules
pip install -r requirements.txt

# Edit the config file and fill in discord information
cd dbot
nano config.toml

# Run the bot
./main
```


## Important Note
Make sure you are authorizing your bot to allowing the bot yo join your server
by using this link and replacing <CLIENT_ID> with your client_id number.
https://discordapp.com/oauth2/authorize?client_id=<CLIENT_ID>&scope=bot


## License
Dbot is licensed under the MIT licence. See LICENCE for details.
