import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, date

from calender_bot.slack_messages.config import * # yeah this is kinda awful but I don't feel like improving it with a real config file
from utils.slack import send_message

def get_volunteer_list(volunteers):
    """Get a comma separated list of volunteers where the last volunteers are separated by ', and'"""
    if len(volunteers) < 2:
        return volunteers[0]

    # Join all but the last element with commas
    comma_separated = ", ".join(volunteers[:-1])

    # Add "and" before the last element
    return f"{comma_separated} and {volunteers[-1]}"

def get_slack_formatted_date(shift_date):
    # convert date to datetime at noon, this will be the time zone of whever teh code is being run
    # which as long as its in the US will be fine since we are only displaying the date.
    date_time = datetime.combine(shift_date, datetime.min.time().replace(hour=12)) 

    return f"<!date^{int(date_time.timestamp())}^{{date}}|{shift_date}>"

def get_day_formatted(day_of_week, shift_date):
    """Get the shift date formatted with slack"""
    formatted_date = get_slack_formatted_date(shift_date)

    date_diff = (shift_date - date.today()).days
    if date_diff <= 0: # should never be less than but for saftey
        return f"*Today* ({formatted_date})"
    elif date_diff < 7:
        return f"this *{day_of_week}* ({formatted_date})"
    else:
        return f"next *{day_of_week}* ({formatted_date})"

def send_volunteer_warning_message(config: MessageConfig, day_of_week, shift_date, volunteers, has_keyholder):
    """
    Sends a warning message if the number of volunteers is below the VOLUNTEER threshold
    or if shift is missing a keyholder
    """
    message = "<!channel> " if config.notify_channel else ""
    message += f"For the shift {get_day_formatted(day_of_week, shift_date)}:\n"

    if len(volunteers) < config.volunteer_threshold:
    
        if len(volunteers) > 0:
            message += f"*•* We need more wrenches! There {'is' if len(volunteers) == 1 else 'are'} only {len(volunteers)} volunteers signed up! ({get_volunteer_list(volunteers)})\n"
        else:
            message += f"*•* We need more wrenches! No one has signed up :cry:\n"
            
        message += f"\t• *Sign up here: <{SHEET_URL}|Calendar>*\n" # respectfully fuck slack for using this weird flavor of "markdown"
    if not has_keyholder:
        # TODO respect config.notify_keyholders
        message += f"*•* We need a keyholder! (Remember to put {config.get_keyholder_marks_list()} after your name if are a keyholder)\n"
        
    logging.info("sending message: " + message)
    send_message(config.channel, message)


def send_special_note_message(config: MessageConfig, day_of_week, shift_date, special_notes):
    """Sends a message to a slack channel with any notes for the shift left in the calendar"""
    message = "<!channel> " if config.notify_channel else ""
    message += f"For the shift {get_day_formatted(day_of_week, shift_date)} there are the following notes:\n"

    for special_note in special_notes:
        message += f"*•* {special_note}\n"
    
    logging.info("sending message: " + message)
    send_message(config.channel, message)

def send_bike_school_message(config: MessageConfig, day_of_week, shift_date, special_notes):
    """Sends a message to a slack channel with any notes for the shift left in the calendar"""
    message = "<!channel> " if config.notify_channel else ""
    message += f"Reminder Bike Skool is {get_day_formatted(day_of_week, shift_date)}! These are the notes:\n"

    for special_note in special_notes:
        message += f"*•* {special_note}\n"
    
    logging.info("sending message: " + message)
    send_message(config.channel, message)