from smtplib import SMTP
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
# EMAIL = "lucas8923890jijkdsfjad@outlook.com"
# PASSWORD = "147874@website"


class NotificationManager:
    def __init__(self):
        pass
    
    def send_email(self, name, email, message):
        with SMTP("smtp.office365.com", port=587) as self.connections:
            self.connections.starttls()
            self.connections.login(user=EMAIL, password=PASSWORD)
            try:
                self.connections.sendmail(from_addr=EMAIL,
                                        to_addrs=EMAIL,
                                        msg=f"Subject:Web Portifolio Contact by {name}\n\n"
                                        f"{name},\n\n{message}\n\nEmail to contact: {email}")
            except UnicodeEncodeError:
                self.connections.sendmail(from_addr=EMAIL,
                                        to_addrs=EMAIL,
                                        msg=f"Subject:Web Portifolio Contact by {str(name).encode(encoding='latin-1',errors='xmlcharrefreplace')}\n\n"
                                        f"{str(name).encode(encoding='latin-1',errors='xmlcharrefreplace')},\n\n"
                                        f"{str(message).encode(encoding='latin-1',errors='xmlcharrefreplace')}\n\nEmail to contact: {email}")