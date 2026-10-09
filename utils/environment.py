from dotenv import load_dotenv
load_dotenv()

import os
from enum import Enum

class EnvVar(Enum):
    # ---- Bike Stand reporting env variables ----
    BIKE_STAND_CHANNEL = ("BIKE_STAND_CHANNEL", True)
    ORG_ID=("ORG_ID", True)
    SURVEY_ID=("SURVEY_ID", True)

    # ---- Calendar env variables ----
    # Can find in the URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}/
    SHEET_ID = ("SHEET_ID", True)
    # variables pointing to the speadsheet/sheet of the config saying when the calendar bot should
    # send slack messages.
    CONFIG_SHEET_ID=("CONFIG_SHEET_ID", False)
    CONFIG_SHEET_GID=("CONFIG_SHEET_GID", False)
    # raw json config that can be used as a fallback to the gsheet, takes precedence over the 
    # default config file
    CALENDAR_BOT_CONFIG=("CALENDAR_BOT_CONFIG", False)

    # ---- Google env variables ----
    GOOGLE_API_KEY=("GOOGLE_API_KEY", True)
    # base64 encoded since I couldn't get raw json to work correctly
    GOOGLE_SERVICE_ACCOUNT=("GOOGLE_SERVICE_ACCOUNT", True)

    # ---- Slack env variables ----
    SLACK_TOKEN=("SLACK_TOKEN", True)

    # ---- Development env variables  ---- 
    # used to override which slack channel messages are sent to
    # useful for development environments to send all slack messages to a testing channel 
    SLACK_CHANNEL_OVERRIDE=("SLACK_CHANNEL_OVERRIDE", False)


    def __new__(cls, env_key: str, required: bool):
        obj = object.__new__(cls)
        obj._value_ = env_key
        obj.required = required
        return obj

    def get(self) -> str | None:
        value = os.environ.get(self.value)
        if value is None and self.required:
            raise EnvironmentError(
                f"Required environment variable '{self.value}' is not set."
            )
        return value

    @classmethod
    def validate_all(cls) -> None:
        """Call at startup to eagerly catch all missing required vars at once."""
        missing = [
            member.value
            for member in cls
            if member.required and os.environ.get(member.value) is None
        ]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")