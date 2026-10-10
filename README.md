# 816 Slack Bot

This repo houses the code for the 816 Slack Bot. The bot is designed to be run once a day in the morning. Functionality:
- Bike Stand Reporting
    - Sends slack messages whenever a new report is submitted 
- Calendar
    - Sends slack messages when:
        - There are not enough volunteers signed up for an upcoming shift
        - There is not a key holder for an upcoming shift
        - There are notes about an upcoming shift
    - Hides past weeks on the Calendar

### High Level File Structure Overview

This is an overview and not a complete list of all files. See directories for further relevant documentation

```
.
├── .github/
│   └── workflows/       - Holds workflows to configuration to run the bot via Github Actions   
├── bike_stand/          - Holds all code for bike stand reporting functionality
├── calendar_bot/        - Holds all code for calendar functionality
│   ├── hide_rows/          - Holds all code for hiding calendar rows
│   ├── slack_messages/     - Holds all code for sending calendar related slack messages
├── utils/               - Holds utilites related to sending slack messages and reading environment variables
│   ├── environment.py      - Documents what environemnt variables are used and what they do
├── main.py              - Runs the bot functionality, parses cli arguments
└── requirements.txt     - Documents what packages must be installed
```

# Running the code
I have tested this code with python 3.10.X and 3.13.X but in theory it should work with anything above 3.10.
I would recommend creating a virtual python environment if you are testing/developing locally.

### 1. Install packages: 
```bash
pip install -r requirements.txt
```

### 2. Setup environment variables
First step is to create a `.env` file in the root directory of the repo. Then go read `utils/environment.py` to see all
environment variables. There are a non-trivial number of environment variables, not all of which are required. However, I will
document some of more complicated ones here.

- `SLACK_TOKEN` - Used for authenticaing with slack to send messages
    - [Slack OAuth Bot Token Documentation](https://docs.slack.dev/authentication/tokens/#bot)
    - Can create a bot (and token) by going to https://api.slack.com/apps and creating an app and adding it to slack
    - When you create a slack bot you must manually add the bot to any channel you want it to be able to post messages in
- `GOOGLE_API_KEY` - Used for authenticating with Google to access Google Sheets
    - See https://handsondataviz.org/google-sheets-api-key.html for a description of how to get one
    - It should be completely free but you will need a google cloud account
- `GOOGLE_SERVICE_ACCOUNT` - Used by hide rows for updating the google sheet
    - See this [documentation](https://sfailabs.com/guides/how-to-get-google-sheets-api-key) for how to get your service account.
    - It should be completely free but you will need a google cloud account
    - I found issues with having json in my .env file when developing locally so you can also base64 encode the json and the program should handle it. 

For the `ORG_ID` and `SURVEY_ID` environment variables, see `bike_stand/README.md`.

When you run `main.py`, it will validate that all required environment variables are present before running any code. 

### 3. Running the code

By default, the program will do nothing when no arguments are given. To see documentation of all of the arguments, do: 
```bash
python main.py --help
```


Example command that performs all functionality
```bash
python main.py --calendar-bot --hide-rows --bike-reports
```

