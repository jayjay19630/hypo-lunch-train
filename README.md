# Hypo Lunch Train

The Hypo Lunch Train is a Slack bot that helps coordinate lunch plans with your team. It allows users to start a "lunch train," join it, and launch it when everyone is ready.

## Features

- Start a lunch train with a simple message.
- Join the lunch train with a button click.
- See who has joined the train, complete with profile pictures.
- Launch the train when everyone is ready to go.

## Requirements

- Python 3.7+
- A Slack workspace with a bot token and app token configured.
- The following environment variables set in a `.env` file:
  - `SLACK_BOT_TOKEN`: Your Slack bot token.
  - `SLACK_APP_TOKEN`: Your Slack app-level token.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/hypo-lunch-train.git
   cd hypo-lunch-train
    ```

2. Install dependencies
    ```
    python -m venv/.venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. Copy .env file and add your Slack tokens

4. Run the app using `python -m app`