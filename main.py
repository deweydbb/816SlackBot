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
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    parser.add_argument(
        "--stand-report-window",
        type=int,
        default=1,
        help="Argument for how many days to look back for new bike stand reports (default: 1)"
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
        send_slack_messages()
        hide_rows()
        send_slack_message_for_new_reports(args.stand_report_window)
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = "Bot encountered error: " + str(e) + " Stack trace: " + stack_trace
        logging.info(error_msg)
                
        send_message("#bot-errors", error_msg)