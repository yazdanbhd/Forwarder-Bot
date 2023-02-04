# Telegram Bot for Broadcasting Messages to Multiple Channels
## Table of contents
* [General info](#general-info)
* [Features](#Features)
* [Requirements](#Requirements)
* [Installation](#Installation)
* [Contributions](#Contributions)

### General info
This bot allows the user to send messages to multiple Telegram channels where the bot has administrative permissions. The channels are stored in the bot's context so that the user doesn't have to enter the list of channels every time they want to broadcast a message.

### Features
* Start the bot by sending the command `/start`.
* Add a channel to the list of channels by sending the command `/add <channel_username>`.
* Remove a channel from the list of channels by sending the command `/remove <channel_username>`.
* Select a channel or send the message to all channels by using the inline keyboard.

### Requirements
* Python 3.x
* `python-telegram-bot` version `13.5`

### Installation
1. Clone this repository to your local machine.
2. Install the required libraries using pip:
```
$ pip install python-telegram-bot==13.15
```
3. Get a bot token from BotFather on Telegram.
4. Replace `YOUR_BOT_TOKEN` in the code with your bot token.
5. Run the bot using:
```
$ python bot.py
```

### Contributions
Feel free to contribute to this project by creating pull requests.
