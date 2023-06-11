import json
from prefect_email import EmailServerCredentials

f = open("./email_creds.json")
email_creds = json.load(f)

credentials = EmailServerCredentials(
    username=email_creds['username'],
    password=email_creds["password"],  # must be an app password
)
credentials.save("email-creds")