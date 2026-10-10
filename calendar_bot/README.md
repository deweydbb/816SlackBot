# Calendar Bot
- Sends slack messages when:
    - There are not enough volunteers signed up for an upcoming shift
    - There is not a key holder for an upcoming shift
        - keyholders can desigate themselves on the calendar by putting '🔑' after their name. (This signifier is configurable. See configuration section below)
    - There are notes about an upcoming shift
        - Example: there is a new volunteer for the shift
        - These notes must have a NON-GRAY background and volunteers signing up for shifts should use a gray/white background to avoid being counted as a note for the shift
- Hides past weeks on the Calendar

## Configuartion
This bot was built to be as flexible as possilbe to allow for easy changes to be made for if example
a new shift day is added or the frequency of messages needs to be adjusted.

There are three sources of configuration that checked in order. If the first source does not exist,
the program moves on to the second source and so on. Souces in order of precedence:
1. Google sheet
    - The configuraiton can be set visually via a google sheet.
    - The sheet to look at is specified by two environment variables: `CONFIG_SHEET_ID` and `CONFIG_SHEET_GID`
        - See `utils/environment.py` for more details
    - See `ExampleConfigSheet.xlsx` for what the current configuration sheet looks like as of writing
2. `CALENDAR_BOT_CONFIG` environment variable 
    - Expected format: `json`
    - See JSON configuraiton section below and `slack_messages/default_config.json` for an example of the format
3. `slack_messages/default_config.json`

### JSON Configuration
The configuration json is json object at the root with three fields:
- `shift_warning`: array of shift warning config objects
    - Each shift warning config object has the following fields:
        - `days`: String array of the list of days the shop is open. (The days of the week to check on the calendar)
        - `days_before`: int, represents how many days out the warning message 
should be sent ahead of the shift
            - So for example if `days` is `Saturday` and `days_before` is `, then the check will be run on Friday
        - `channel`: String, name of slack channel to send messages to. (must begin with `#`)
        - `notify_channel`: boolean, whether to include `@channel` in message
        - `notify_keyholders`: boolean, not implemented
        - `keyholder_marks`: String array that identifies as volunteer as a keyholder
            - If not specified, defaults to 🔑
        - `volunteer_threshold`: int, Minimum number of volunteers needed for a shift. Any less will cause the warning message to be sent
- `shift_notes`: array of shift note config objects
    - Each shift notes config object has the following fields:
        - `days`: String array of the list of days the shop is open. (The days of the week to check on the calendar)
        - `days_before`: int, represents how many days out the warning message 
should be sent ahead of the shift
            - So for example if `days` is `Saturday` and `days_before` is `, then the check will be run on Friday
        - `channel`: String, name of slack channel to send messages to. (must begin with `#`)
        - `notify_channel`: boolean, whether to include `@channel` in message
- `bike_school_reminder`: array of bike school reminder config objects
    - Each bike school reminder config object has the following fields:
        - `days`: String array of the list of days the shop is open. (The days of the week to check on the calendar)
        - `days_before`: int, represents how many days out the warning message 
should be sent ahead of the shift
            - So for example if `days` is `Saturday` and `days_before` is `, then the check will be run on Friday
        - `channel`: String, name of slack channel to send messages to. (must begin with `#`)
        - `notify_channel`: boolean, whether to include `@channel` in message
        - `bikeschool_marks`: String array that identifies an event as bike school if it includes ones of the strings