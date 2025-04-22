import os
from slack_bolt import App
from dotenv import load_dotenv

from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables from .env file
load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Constants
LUNCH_TRAIN_STARTED_TEXT = "*The Hypo Lunch Train has been started by <@{user}>. All aboard!*"
HUNGRY_CARRIAGE_TEXT = ":hamburger: *Super Hungry Carriage People*\nOnly for the hungriest SG office peeps."
JOIN_BUTTON = {
    "type": "button",
    "text": {"type": "plain_text", "emoji": True, "text": "Join!"},
    "action_id": "join_lunch_train_action",
}
LAUNCH_BUTTON = {
    "type": "button",
    "text": {"type": "plain_text", "emoji": True, "text": "We're ready, LET'S GO!"},
    "action_id": "launch_lunch_train_action",
}

@app.message("Lunch!!!")
def message_lunch_train(message, say):
    global lunch_train_participants
    global lunch_train_starter
    lunch_train_participants = []  # Reset participants when a new lunch train starts
    lunch_train_starter = message["user"]

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": LUNCH_TRAIN_STARTED_TEXT.format(user=message["user"])},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": HUNGRY_CARRIAGE_TEXT},
            "accessory": JOIN_BUTTON,
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "Looks like nobody's here yet..."},
                {"type": "plain_text", "emoji": True, "text": "0 people"},
            ],
        },
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [LAUNCH_BUTTON],
        },
    ]

    # Send the initial message and store the timestamp for updates
    response = say(
        blocks=blocks,
        text=LUNCH_TRAIN_STARTED_TEXT.format(user=message["user"]),
    )
    global lunch_train_message_ts
    lunch_train_message_ts = response["ts"]  # Store the message timestamp


@app.action("join_lunch_train_action")
def join_lunch_train_action(body, ack, client):
    # Acknowledge the action
    ack()

    user_id = body["user"]["id"]
    global lunch_train_starter
    global lunch_train_participants
    global lunch_train_message_ts

    if user_id not in lunch_train_participants:
        lunch_train_participants.append(user_id)

        # Fetch user info to get profile pictures
        participants_elements = []
        for user in lunch_train_participants:
            user_info = client.users_info(user=user)
            profile_image = user_info["user"]["profile"]["image_48"]
            display_name = user_info["user"]["real_name"]

            participants_elements.append(
                {
                    "type": "image",
                    "image_url": profile_image,
                    "alt_text": display_name,
                }
            )

        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": LUNCH_TRAIN_STARTED_TEXT.format(user=lunch_train_starter)},
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": HUNGRY_CARRIAGE_TEXT},
                "accessory": JOIN_BUTTON,
            },
            {
                "type": "context",
                "elements": participants_elements
                + [
                    {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"{len(participants_elements)} people",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "actions",
                "elements": [LAUNCH_BUTTON],
            },
        ]

        # Use the Slack client to update the message
        client.chat_update(
            channel=body["channel"]["id"],
            ts=lunch_train_message_ts,
            blocks=blocks,
            text=LUNCH_TRAIN_STARTED_TEXT.format(user=lunch_train_starter),
        )
    else:
        # Send a message indicating the user is already in the lunch train
        client.chat_postEphemeral(
            channel=body["channel"]["id"],
            user=user_id,
            text="You are already in the lunch train!",
        )


@app.action("launch_lunch_train_action")
def launch_lunch_train_action(body, ack, client):
    # Acknowledge the action
    ack()

    global lunch_train_starter
    global lunch_train_participants
    global lunch_train_message_ts

    # Fetch user info to get profile pictures
    participants_elements = []
    for user in lunch_train_participants:
        user_info = client.users_info(user=user)
        profile_image = user_info["user"]["profile"]["image_48"]
        display_name = user_info["user"]["real_name"]

        participants_elements.append(
            {
                "type": "image",
                "image_url": profile_image,
                "alt_text": display_name,
            }
        )

    if len(lunch_train_participants) > 1:
        launch_train_text = "The *Hypo Lunch Train* is now setting off. All aboard for sustenance! *WOOHOO*"
    elif len(lunch_train_participants) == 1:
        user = lunch_train_participants[0]
        launch_train_text = (
            f"Nobody joined the lunch train except for <@{user}>, so sad..."
        )
    else:
        launch_train_text = "The lunch train is empty today. Looks like Eve is handing out lots of tasks."

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": LUNCH_TRAIN_STARTED_TEXT.format(user=lunch_train_starter)},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": HUNGRY_CARRIAGE_TEXT},
        },
        {
            "type": "context",
            "elements": participants_elements
            + [
                {
                    "type": "plain_text",
                    "emoji": True,
                    "text": f"{len(lunch_train_participants)} people",
                },
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": launch_train_text},
        },
    ]

    # Use the Slack client to update the message
    client.chat_update(
        channel=body["channel"]["id"],
        ts=lunch_train_message_ts,
        blocks=blocks,
        text="*The lunch train has started moving. Let's eat!!!*",
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()