from typing import List
import requests
import os


class Mailgun:
    FROM_TITLE = "Stores Rest APi"
    FROM_EMAIL = os.environ.get("FROM_EMAIL")
    API_KEY = os.environ.get("API_KEY")
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    print("gun", MAILGUN_DOMAIN)
    print("api", API_KEY)
    print("email", FROM_EMAIL)

    @classmethod
    def send_email(
        cls, emails: [List], subject: str, text: str, html: str
    ) -> requests.Response:
        return requests.post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": emails,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )


# PYTHONUNBUFFERED=1;MAILGUN_DOMAIN=sandboxfea8bb8ea91a4f0b818ba8751671f502.mailgun.org;API_KEY=003c5256dcaee9731daade8325a3740c-4de08e90-48e5a758;FROM_EMAIL=brad@sandboxfea8bb8ea91a4f0b818ba8751671f502.mailgun.org

# MAILGUN_DOMAIN=sandboxfea8bb8ea91a4f0b818ba8751671f502.mailgun.org
# API_KEY=003c5256dcaee9731daade8325a3740c-4de08e90-48e5a758
# FROM_EMAIL=brad@sandboxfea8bb8ea91a4f0b818ba8751671f502.mailgun.org
