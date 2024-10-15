# Discord Voice Bot

## Description

A Discord bot that reads text commands and speaks in voice channels. The bot can:

- Speak a given message in a voice channel using the `!say` command.
- Automatically disconnect from the voice channel after 1 minute of inactivity, saying "Bye".
- Manually disconnect from the voice channel using the `!saynomore` command, with the bot saying "Bye" before disconnecting.


## Prerequisites

- **Python 3.7 or higher**
- **FFmpeg** installed and added to your system PATH.
  - **Windows**: Download from [FFmpeg Downloads](https://ffmpeg.org/download.html#build-windows).
  - **macOS**: Install via Homebrew: `brew install ffmpeg`.
  - **Linux**: Install via package manager, e.g., `sudo apt-get install ffmpeg`.

## Installation

1. **Clone the repository**:


   git clone https://github.com/benrosiers/discord_voice_bot.git
   cd discord_voice_bot
   
2.**Create and activate a virtual environment (recommended)**:

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Unix or macOS:
source venv/bin/activate

3.**Install the dependencies**:

pip install -r requirements.txt

4.**Set up the environment variables for your bot token and secret**:

# Unix/Linux/macOS

export BOT_TOKEN='your-bot-token-here'
export BOT__SEC='your-bot-secret-here'


# Windows Command Prompt

set BOT_TOKEN=your-bot-token-here
set BOT__SEC=your-bot-secret-here

# Windows PowerShell

$env:BOT_TOKEN="your-bot-token-here"
$env:BOT__SEC="your-bot-secret-here"

Important: Replace 'your-bot-token-here' and 'your-bot-secret-here' with your actual bot token and secret. Never share your bot token or secret publicly.

## Usage

1.**Run the bot**:

python main.py

2.**Use the bot in Discord**:

In a text channel, type:

!say Hello, this is a test message.

The bot will join a voice channel according to the logic defined and speak the message.

# Packaging the Application

If you wish to install the application as a package:

1.**Build the package**:

python setup.py sdist bdist_wheel

2.**Install the package**:

pip install dist/discord_voice_bot-0.1.0-py3-none-any.whl

3.**Run the bot using the console script**

discord-voice-bot

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Benoit Desrosiers at benoitdesrosiers1980@gmail.com.