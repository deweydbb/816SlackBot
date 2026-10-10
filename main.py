import logging
import traceback
import argparse
import sys

from bike_stand.bike_stand_reports import send_slack_message_for_new_reports
from calendar_bot import send_slack_messages, hide_rows

from utils.environment import EnvVar
from utils.slack import send_message

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--calendar-bot",
        action='store_true',
        help="Send slack messages for the Calendar (low volunteers, missing keyholder)"
    )
    parser.add_argument(
        "--hide-rows",
        action='store_true',
        help="Hide previous weeks on the Calendar sheet"
    )
    parser.add_argument(
        "--stand-reports",
        action='store_true',
        help="Send slack messages for new bike stand reports"
    )
    parser.add_argument(
        "--stand-report-window",
        type=int,
        default=1,
        help="Argument for how many days to look back for new bike stand reports (default: 1)"
    )
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

    # Validate all necessary environment variables are populated
    EnvVar.validate_all()

    try:
        if args.calendar_bot:
            send_slack_messages()
        if args.hide_rows:
            hide_rows()
        if args.stand_reports:
            send_slack_message_for_new_reports(args.stand_report_window)
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = "Bot encountered error: " + str(e) + " Stack trace: " + stack_trace
        logging.error(error_msg)
                
        send_message("#bot-errors", error_msg)