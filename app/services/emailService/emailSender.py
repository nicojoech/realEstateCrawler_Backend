import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.emailService.config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT


def format_listings(listings: list) -> str:
    """
    Formats the given listings into a string
    :param listings: list of listings to format
    :return: formatted string
    """
    formatted_listings = []
    for listing in listings:
        # Format the address
        address_parts = [listing['address'][part] for part in ['zip_code', 'state', 'city', 'street', 'district'] if
                         listing['address'].get(part)]
        address = ', '.join(address_parts)

        # Format the listing details
        details = (
            f"Link: https://www.willhaben.at{listing['link']}\n"
            f"Title: {listing.get('title') or 'N/A'}\n"
            f"Address: {address}\n"
            f"Area: {listing.get('area')}m²\n"
            f"Rooms: {listing.get('number_of_rooms')}\n"
            f"Additional Info: {listing.get('additional_info', 'N/A')}\n"
            f"Price: €{listing.get('price')}\n"
        )

        formatted_listings.append(details)

    return "\n\n".join(formatted_listings)


def is_valid_email(email: str) -> bool:
    """
    Checks if the given email address is valid using a regex pattern
    :param email: email address to check
    :return: True if the email address is valid, False otherwise
    """
    pattern = re.compile(r'^[\w.-]+@[\w.-]+\.\w+$')
    return pattern.match(email) is not None


def create_message(crawler_name: str, receiver: str, subject: str, body: str) -> str:
    """
    Creates a MIME message with the given receiver and body and returns it as a string.
    Subject is set to "RealEstateCrawler - Notification". To be changed later on
    either Matching Listings found or simply Notification still running
    :param crawler_name: name of the crawler
    :param subject:  subject of the email
    :param receiver: email address of the receiver goes through a check for syntax validity
    :param body: content of the email
    :return: MIME message as a string
    """
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = receiver
    message["Subject"] = f"{crawler_name} - {subject}"
    message.attach(MIMEText(body, "plain"))

    return message.as_string()


def send(crawler_name: str, receiver: str, subject: str, body: str) -> None:
    """
    Sends an email to the given receiver with the given body
    Does not send if the receiver is not a valid email address
    :param crawler_name:
    :param subject:
    :param receiver:
    :param body:
    :return:
    """
    if not is_valid_email(receiver):
        print(f"Invalid email address: {receiver}")
        return

    message = create_message(crawler_name, receiver, subject, body)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # server.set_debuglevel(0)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, receiver, message)
        print(f"Successfully sent email to {receiver}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# def main():
#     #send("Test Crawler", "wi21b026@technikum-wien.at", "Testing Email Service", "This is a test email.")
#
# if __name__ == '__main__':
#     main()
