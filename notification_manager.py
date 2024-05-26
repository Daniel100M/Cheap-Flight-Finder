import os
import smtplib

from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.environ['ACCOUNT_SID']
        self.auth_token = os.environ['AUTH_TOKEN']
        self.email = "danielmakmal14@gmail.com"

    def send_sms(self, body: str) -> None:
        """
        Sends a text message to my phone.
        :param body: Text content.
        :return:
        """
        client = Client(self.account_sid, self.auth_token)

        # This will send the text message.
        message = client.messages \
            .create(
            body=body,
            from_='+16504222306',
            to='+972558844853'
        )

        print(message.status)  # Checking if the message was sent successfully.

    def send_email(self, recipient_email, sbj, msg):
        """
        Sends email from one address to another.
        :param recipient_email:
        :param sbj: Email subject (String).
        :param msg: Email message (String).
        :return:
        """
        password = "wpgjhbhkvnhwyyys"
        recipient = recipient_email

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email, password=password)
            connection.sendmail(from_addr=self.email,
                                to_addrs=recipient,
                                msg=f"Subject: {sbj}\n\n"
                                    f"{msg}")
