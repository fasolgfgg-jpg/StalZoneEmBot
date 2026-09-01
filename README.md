# StalCraft Emission Monitor Bot

A Telegram bot that automatically monitors and notifies about emission events in the StalCraft game. The bot tracks the StalCraft API for upcoming emissions and sends timely notifications to a designated Telegram channel with event details and current player count.

## Features

- 🔔 **Real-time Emission Detection** - Monitors StalCraft API every 25 seconds for upcoming emission events
- 📢 **Automatic Channel Notifications** - Posts emission alerts to [@InformSCX](https://t.me/InformSCX) Telegram channel
- 🎮 **Player Count Tracking** - Includes current online player count from Steam API
- 🕐 **Timezone Conversion** - Automatically converts UTC timestamps to Moscow Standard Time (MSK)
- 📸 **Visual Notifications** - Sends notifications with emission-themed images
- 🧹 **Message Management** - Automatically cleans up previous "emission ended" messages
- 🔄 **Continuous Monitoring** - Runs 24/7 with separate threads for bot commands and emission checking

## Requirements

- Python 3.7+
- pyTelegramBotAPI (telebot)
- requests
- Telegram Bot Token
- StalCraft API credentials (Client ID and Client Secret)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stalcraft-emission-bot.git
cd stalcraft-emission-bot
```

2. Install required dependencies:
```bash
pip install pyTelegramBotAPI requests
```

3. Create a `.env` file or `keys.json` based on the template:
```bash
cp .env.example .env
```

4. Configure your environment variables (see Configuration section below)

## Configuration

### Environment Variables

Create a `keys.json` file in the project root with the following structure:

```json
{
    "TG-Client-Token": "your_telegram_bot_token_here",
    "Client-Secret": "your_stalcraft_client_secret_here",
    "Client-ID": "your_stalcraft_client_id_here"
}
```

Or use `.env.example` as a template:

- **TG_CLIENT_TOKEN** - Your Telegram Bot API token (obtain from [@BotFather](https://t.me/BotFather))
- **CLIENT_SECRET** - Your StalCraft API Client Secret
- **CLIENT_ID** - Your StalCraft API Client ID

### Getting StalCraft API Credentials

1. Visit the [StalCraft API documentation](https://eapi.stalcraft.net/)
2. Register your application to receive Client ID and Client Secret
3. Add these credentials to your `keys.json` configuration file

## Usage

Run the bot:
```bash
python Main.py
```

The bot will:
1. Start polling for Telegram commands (`/start`, `/help`)
2. Begin monitoring StalCraft emission API in a background thread
3. Send notifications to [@InformSCX](https://t.me/InformSCX) when emissions are detected (within 30 seconds of predicted start time)
4. Post "emission ended" messages 4 minutes after emission starts
5. Clean up previous emission notifications automatically

### Bot Commands

- `/start` - Get information about the bot and channel link
- `/help` - Display help information and channel link

## Project Structure

```
stalcraft-emission-bot/
├── Main.py              # Main bot entry point and emission checker
├── Tools.py             # Utility functions for token reading and API calls
├── Debug.py             # Logging utilities
├── GetOnline.py         # Steam player count fetcher
├── JsonMaster.py        # JSON handling utilities
├── keys.json            # Configuration file (not committed to git)
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
├── photo.png           # Emission notification image
├── photo1.png          # Alternative notification image
├── MessageID.ids       # Tracks message IDs for cleanup
└── name.nlf            # Name configuration
```

## How It Works

1. **Emission Monitoring**: The `check()` function runs in a separate thread, polling the StalCraft emission API every 25 seconds
2. **Detection Logic**: When the current UTC time is within 30 seconds of the predicted emission start time, the bot triggers a notification
3. **Notification**: The `sender()` function posts to the Telegram channel with:
   - Emission photo
   - Start time in MSK timezone
   - Current online player count
4. **Cleanup**: After 4 minutes, posts an "emission ended" message and deletes any previous ended messages to keep the channel clean

## Logging

The bot logs all operations to the `Logs/` directory using the Debug module:
- Emission checks
- API responses
- Message sending operations
- Error handling

## Channel

Official channel: [@InformSCX](https://t.me/InformSCX)

## License

This project is provided as-is for monitoring StalCraft game emissions.

## Notes

- The bot requires continuous operation to monitor emissions effectively
- Ensure your Telegram bot has permission to post to the target channel
- The emission API endpoint: `https://eapi.stalcraft.net/RU/emission`
- Player count source: Steam API for StalCraft (AppID: 1818450)
