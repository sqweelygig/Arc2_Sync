from smtplib import SMTP
from time import strftime

from bin.Interface import Interface


class Email(Interface):
    def __init__(self, mail_to, mail_server, mail_username, mail_password):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.to_address = mail_to
        self.server = mail_server
        self.username = mail_username
        self.password = mail_password
        self.body = strftime('%c') + "\r\n"
        self.send = False

    @staticmethod
    def get_requirements():
        return Interface.get_requirements() | {"mail_to", "mail_server", "mail_username", "mail_password"}

    def reassure(self, output=""):
        try:
            super().reassure(output)
        except NotImplementedError:
            pass
        from time import strftime
        print(strftime("%c") + " - " + output)

    def put(self, output=""):
        try:
            super().put(output)
        except NotImplementedError:
            pass
        self.send = True
        self.reassure(output)
        self.body += output + "\r\n"

    def get(self, key=""):
        try:
            super().get(key)
        except NotImplementedError:
            pass
        self.put(key+"?")
        raise NotImplementedError

    def __del__(self):
        if self.send:
            self.body += strftime('%c') + "\r\n"
            server = SMTP(self.server)
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            msg = "\r\n".join([
                "From: " + self.username,
                "To: " + self.to_address,
                "Subject: Arc Synchronise Results",
                "",
                self.body,
            ])
            server.sendmail(self.username, self.to_address, msg.encode('utf-8'))
