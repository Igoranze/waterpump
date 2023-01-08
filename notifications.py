"""
This file sends notifications when the pump starts and when the pump ends
"""
import os
from dotenv import load_dotenv

import requests
from json import dumps
import smtplib
import ssl

from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()


def send_email(water_pump_started=None):
    if water_pump_started is None:
        raise Exception('No water pump message notifications')

    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))

    to = [os.getenv('TO_RECIPIENT')]

    ssl_context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=ssl_context)
        server.ehlo()  # Can be omitted
        server.login(gmail_user, gmail_password)

        for email in to:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = f'Water pump started: {water_pump_started}'
            mail['From'] = gmail_user
            mail['To'] = email

            text_template = f"""
                Water pump started: {water_pump_started}
    
                at {datetime.now()},
                """

            text_content = MIMEText(text_template, 'plain')

            mail.attach(text_content)

            server.sendmail(gmail_user, email, mail.as_string())

        server.quit()


def push_webhook_cardv2(water_pump_started=None):
    if water_pump_started is None:
        raise Exception('No water pump message notifications')

    webhook_url = os.getenv('GOOGLE_WEBHOOK_URL')

    bot_message = {
        "cardsV2": [
            {
                "cardId": "uiid",
                "card": {
                    "header": {
                        "title": f"water pump started: {water_pump_started}",
                        "imageUrl":
                            "https://media.tenor.com/nTfGANr9MlAAAAAi/lord-of-the-rings-my-precious.gif",
                        "imageType": "CIRCLE",
                        "imageAltText": "Avatar",
                    },
                    "sections": [
                        {
                            "header": "Pompje",
                            "collapsible": False,
                            "uncollapsibleWidgetsCount": 1,
                            "widgets": [
                                {
                                    "decoratedText": {
                                        "startIcon": {
                                            "knownIcon": "DESCRIPTION",
                                        },
                                        "text": f"{datetime.now()}"
                                    },
                                }
                            ],
                        },
                    ],
                },
            }
        ],
    }

    message_headers = {"Content-Type": "application/json; charset=UTF-8"}

    response = requests.post(
        webhook_url,
        data=dumps(bot_message),
        headers=message_headers
    )

