from dotenv import load_dotenv
load_dotenv()

from datetime import date, timedelta
import logging
import traceback
import argparse
import sys

from calender_bot.config import send_message
from calender_bot.bike_stand_reports import send_slack_message_for_new_reports
from calender_bot.calender_bot import send_slack_messages
from calender_bot.hide_rows import hide_rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        send_slack_messages()
        # hide_rows()
        # send_slack_message_for_new_reports(1)
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = "Bot encountered error: " + str(e) + " Stack trace: " + stack_trace
        logging.info(error_msg)
                
        send_message("#bot-tester", error_msg)

    # TODO send slack message on error