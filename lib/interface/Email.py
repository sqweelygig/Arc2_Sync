from smtplib import SMTP
from time import strftime

from lib.interface.Relay import Relay


class Email(Relay):
    def get(self, key=""):
        super().get(key)

    def __init__(self, mail_to, mail_server, mail_from, mail_password):
        super().__init__(mail_to, mail_server, mail_from)
        self.password = mail_password

    @staticmethod
    def get_requirements():
        return Relay.get_requirements() | {"mail_password"}

    def __del__(self):
        if self.send:
            self.body += strftime('%c') + "\r\n"
            server = SMTP(self.server)
            server.ehlo()
            server.starttls()
            server.login(self.mail_from, self.password)
            msg = "\r\n".join([
                "From: " + self.mail_from,
                "To: " + self.to_address,
                "Subject: Arc Synchronise Results",
                "",
                self.body,
            ])
            server.sendmail(self.mail_from, self.to_address, msg.encode('utf-8'))
