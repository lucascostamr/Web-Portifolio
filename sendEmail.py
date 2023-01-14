from smtplib import SMTP
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

class NotificationManager:
    def __init__(self):
        pass
    
    def send_email(self, name, email, message):
        with SMTP("smtp.office365.com", port=587) as self.connections:
            self.connections.starttls()
            self.connections.login(user=EMAIL, password=PASSWORD)
            try:
                self.connections.sendmail(from_addr=EMAIL,
                                        to_addrs=TO_EMAIL,
                                        msg=f"Subject:Web Portifolio Contact by {str(name).encode(encoding='latin-1',errors='xmlcharrefreplace')}\n\n"
                                        f"{str(name).encode(encoding='latin-1',errors='xmlcharrefreplace')},\n\n"
                                        f"{str(message).encode(encoding='latin-1',errors='xmlcharrefreplace')}\n\nEmail to contact: {email}")
            except:
                pass