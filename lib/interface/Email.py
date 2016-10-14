from smtplib import SMTP

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
        self.body = ""

    @staticmethod
    def get_requirements():
        return Interface.get_requirements() | {"mail_to", "mail_server", "mail_username", "mail_password"}

    def reassure(self, output=""):
        try:
            super().reassure(output)
        except NotImplementedError:
            pass

    def put(self, output=""):
        try:
            super().put(output)
        except NotImplementedError:
            pass
        self.body += output + "\r\n"

    def get(self, key=""):
        try:
            super().get(key)
        except NotImplementedError:
            pass
        self.put(key+"?")
        raise NotImplementedError

    def __del__(self):
        server = SMTP(self.server)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.username, self.to_address, "\r\n".join([
            "From: " + self.username,
            "To: " + self.to_address,
            "Subject: Arc Synchronise Results",
            "",
            self.body,
        ]))