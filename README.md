Sure, here's a basic README for your code:

# Pool Tracker Bot

This is a Telegram bot built with Pyrogram that allows users to track pools on a decentralized exchange (DEX). The bot uses the Stonfi API to fetch pool data and store it in a SQLite database. Users can add pools to their watchlist and view detailed information about them.

## Features

- `/start`: Welcome message
- `/about`: Information about the bot
- `/get_quantity_pools`: Get the number of pools in the database
- `/get_info_by_pool`: Get detailed information about a specific pool
- `/top10_pools`: Get the top 10 pools based on TVL (To be implemented)
- `/show_watchlist`: Show the user's watchlist

## Prerequisites

- Python 3.6 or higher
- A Telegram bot token (you can create one using the BotFather on Telegram)
- A Stonfi API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pool-tracker-bot.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `config.py` file in the root directory and add your Telegram bot token and Stonfi API key:

```python
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'
stonfi_api_key = 'YOUR_STONFI_API_KEY'
```

4. Run the bot:

```bash
python bot.py
```

## Usage

- Start the bot on Telegram and send the `/start` command to receive a welcome message.
- Use the `/about` command to learn more about the bot.
- Use the `/get_quantity_pools` command to get the number of pools in the database.
- Use the `/get_info_by_pool` command to get detailed information about a specific pool.
- Use the `/top10_pools` command to get the top 10 pools based on TVL (To be implemented).
- Use the `/show_watchlist` command to view your watchlist.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
