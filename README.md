# File-Forward-Bot

A simple telegram bot to forward files from one channel to another.

### Features

- Forward files from a source channel to a target channel.
- Skip a specific number of messages.
- Cancel the forwarding process.

### Prerequisites

- Python 3.8+
- A telegram bot token.
- Your telegram API ID and API HASH.
- A MongoDB database URI.

### Environment Variables

- `API_ID` - Your telegram API ID.
- `API_HASH` - Your telegram API HASH.
- `BOT_TOKEN` - Your telegram bot token.
- `SESSION` - A custom session name.
- `LOG_CHANNEL` - The ID of the channel where the bot will send logs.
- `PORT` - The port on which the web server will run.
- `ADMINS` - A list of user IDs of the bot admins.
- `DB_URI` - Your Mongo DB URI obtained from cloud.mongodb.com
- `DB_NAME` - Your Mongo DB Database name. Same as the one you entered in DB URI, if any.

### Running the bot

1. Clone the repository:
   ```
   git clone https://github.com/Joelkb/File-Forward-Bot
   ```
2. Create a `.env` file with the following content:
   ```
   API_ID=12345
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   SESSION=your_session_name
   LOG_CHANNEL=-1001234567890
   PORT=8080
   ADMINS=123456789
   DB_URI=your_db_uri
   DB_NAME=your_db_name
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python3 bot.py
   ```

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/Joelkb/File-Forward-Bot">
     <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
  </a>
</p>
