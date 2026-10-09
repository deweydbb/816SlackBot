from datetime import date, timedelta

from calender_bot.bike_stand_reports import send_slack_message_for_new_reports
from calender_bot.calender_bot import send_slack_messages
from calender_bot.hide_rows import hide_rows

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    # send_slack_messages()
    hide_rows()
    # send_slack_message_for_new_reports(1)

    # TODO send slack message on error