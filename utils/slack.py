import logging
import time

from utils.environment import EnvVar

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TOO_MANY_REQUESTS_CODE = 429

def _send_message_internal(channel_id, message, use_blocks, fallback_text):
    slack_token = EnvVar.SLACK_TOKEN.get()
    if slack_token is None:
        logging.error("Slack API token iis missing")

    client = WebClient(token=slack_token)

    if use_blocks:
        return client.chat_postMessage(
            channel=channel_id,
            text=fallback_text,
            blocks=message
        )
    
    return client.chat_postMessage(
        channel=channel_id,
        text=message,
    )

def send_message(channel_id, message, use_blocks=False, fallback_text=None):
    """Send the given message to the specified channel and respect rate limits"""

    channel_override = EnvVar.SLACK_CHANNEL_OVERRIDE.get()
    if channel_override is not None:
        logging.info(f"Would have send message to {channel_id}, sending to {channel_override} instead")
        channel_id = channel_override

    try:
        # Sending a message to the specified Slack channel
        _send_message_internal(channel_id, message, use_blocks, fallback_text)
        logging.info(f"Message sent successfully")
        logging.debug(f"Message sent: {message}")
    except SlackApiError as e:
        if e.response.status_code == TOO_MANY_REQUESTS_CODE:
            # The `Retry-After` header will tell you how long to wait before retrying
            delay = int(e.response.headers['Retry-After'])
            logging.info(f"Rate limited. Retrying in {delay} seconds")
            time.sleep(delay)
            _send_message_internal(channel_id, message, use_blocks, fallback_text)
        else:
            logging.error(f"Error sending message: {e}")