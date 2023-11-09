# Confluence 2023 Discord Bot

This bot is designed to run using Python and the Discord.py library.

## Installation Steps

1. Clone the repository.
2. Install the required dependencies using pip: `pip install -r requirements.txt`
3. Rename the `.sample.env` file to `.env` and fill in the required fields.
4. Run the bot by executing the Python script.
```bash
python bot.py
```

## Commands

- Use the following commands in Discord after inviting the bot to a server:

    - `/sendmessage <message or link>`: Sends a message to the current channel.
    - `/editmessage <link> <message_id>`: Edits a message in the current channel.
    - `/sendgif <link>`: Sends a GIF to the current channel.
    - `$flag`: Sends the flag if you direct message the bot.