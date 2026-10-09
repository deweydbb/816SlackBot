import requests
import traceback
import logging

from datetime import datetime
from zoneinfo import ZoneInfo

from utils.environment import EnvVar
from utils.slack import send_message

def get_new_bike_reports(interval: int):
    ORG_ID = EnvVar.ORG_ID.get()
    SURVEY_ID = EnvVar.SURVEY_ID.get()
    FEATURE_URL = f"https://services.arcgis.com/{ORG_ID}/arcgis/rest/services/survey123_{SURVEY_ID}_results/FeatureServer/0"

    # Query new features
    params = {
        "where": f"CreationDate >= CURRENT_TIMESTAMP - INTERVAL '{interval}' DAY",
        "outFields": "CreationDate,Creator,additional_details,email,station_location_copy,name,objectid,what_is_the_problem,what_is_the_problem_other,globalid",
        "f": "json",
        "returnGeometry": "false",
        "resultRecordCount": 2000
    }

    resp = requests.get(FEATURE_URL + "/query", params=params).json()

    logging.info(f"query reports in last day: {resp}")

    features = resp.get("features", [])

    reports = []

    for feat in features:
        oid = feat["attributes"]["objectid"]

        # Get list of attachments
        attach_url = f"{FEATURE_URL}/{oid}/attachments"
        attachments = requests.get(attach_url, params={"f": "json"}).json()

        attachment_urls = []

        for att in attachments.get("attachmentInfos", []):
            att_id = att["id"]
            attachment_urls.append(f"{attach_url}/{att_id}")

        problems = []

        if feat["attributes"]["what_is_the_problem"] is not None:
            problems = feat["attributes"]["what_is_the_problem"].split(',')
        # what_is_the_problem_other captures the text response if the user selects other for the problem
        if feat["attributes"]["what_is_the_problem_other"] is not None:
            problems.append(feat["attributes"]["what_is_the_problem_other"])

        globalId = feat["attributes"]["globalid"]
        viewUrl = f"https://survey123.arcgis.com/share/{SURVEY_ID}?mode=view&globalId={globalId}"

        reports.append({
            "DateReported": feat["attributes"]["CreationDate"],
            "ReporterName": feat["attributes"]["name"],
            "ReporterEmail": feat["attributes"]["email"],
            "StandLocation": feat["attributes"]["station_location_copy"],
            "problems": problems,
            "additionalDetails": feat["attributes"]["additional_details"],
            "attachments": attachment_urls,
            "viewUrl": viewUrl
        })

    return reports

def get_reported_date(report):
    report_millis = report['DateReported']

    report_secs = int(report_millis / 1000)

    dt_utc = datetime.fromtimestamp(report_secs)
    dt_central = dt_utc.astimezone(ZoneInfo("America/Chicago"))

    fallback = dt_central.strftime("%Y-%m-%d %I:%M:%S %p %Z")

    return f"<!date^{report_secs}^{{date_short}} at {{time}}|{fallback}>"

def get_reporter_details(report):
    reporter_name = report['ReporterName']
    reporter_email = report['ReporterEmail']

    if reporter_name is None and reporter_email is None:
        return None

    if reporter_name is None and reporter_email is not None:
        return reporter_email

    if reporter_name is not None and reporter_email is None:
        return reporter_name

    return f"{reporter_name} ({reporter_email})"

def send_slack_message_for_new_reports(interval=1):
    try:
        reports = get_new_bike_reports(interval)

        logging.info(f"reports = {reports}")

        for report in reports:
            message = f"New <{report['viewUrl']}|Report> for {report['StandLocation']} Maintenance Stand\n"

            message += f"*•* Reported on {get_reported_date(report)}:\n"

            message += '*•* Problems:\n'

            for problem in report['problems']:
                message += f"\t*•* {problem}\n"

            additional_details = report['additionalDetails']
            if additional_details is not None:
                message += f"*•* Additional Details: {additional_details}\n"

            reporter = get_reporter_details(report)
            if reporter is not None:
                message += f"*•* Reporter: {reporter}\n"

            attachments = report['attachments']
            if len(attachments) > 0:
                formatted_urls = ", ".join(f"<{url}|Photo>" for url in attachments)
                message += f"*•* {formatted_urls}"

            logging.info("sending bike report message in slack: " + message)

            channel = EnvVar.BIKE_STAND_CHANNEL.get()

            send_message(channel, message)
    except Exception as e:
        # if failed to run send a message to the bot tester so someone is aware of the failure 
        stack_trace = traceback.format_exc()
        error_msg = "Bot encountered error sending bike stand report messages. Error: " + str(e) + " Stack trace: " + stack_trace
        logging.error(error_msg)
        
        send_message("#bot-tester", error_msg)

        raise e
