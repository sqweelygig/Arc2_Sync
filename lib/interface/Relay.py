from smtplib import SMTP
from time import strftime

from bin.Interface import Interface


class Relay(Interface):
    def __init__(self, mail_to, mail_server, mail_from):
        try:
            super().__init__()
        except NotImplementedError:
            pass
        self.to_address = mail_to
        self.server = mail_server
        self.mail_from = mail_from
        self.body = strftime('%c') + "\r\n"
        self.send = False

    @staticmethod
    def get_requirements():
        return Interface.get_requirements() | {"mail_to", "mail_server", "mail_from"}

    def reassure(self, output=""):
        try:
            super().reassure(output)
        except NotImplementedError:
            pass
        from time import strftime
        print(strftime("%c") + " - " + output)

    def put(self, output="", is_content=True):
        try:
            super().put(output)
        except NotImplementedError:
            pass
        self.send = self.send or is_content
        self.reassure(output)
        self.body += output + "\r\n"

    def get(self, key=""):
        try:
            super().get(key)
        except NotImplementedError:
            pass
        self.put(key+"?")
        # There is no way of interrogating an e-mail address
        raise NotImplementedError

    def __del__(self):
        if self.send:
            self.body += strftime('%c') + "\r\n"
            server = SMTP(self.server)
            server.ehlo()
            msg = "\r\n".join([
                "From: " + self.mail_from,
                "To: " + self.to_address,
                "Subject: Arc Synchronise Results",
                "",
                self.body,
            ])
            server.sendmail(self.mail_from, self.to_address, msg.encode('utf-8'))
