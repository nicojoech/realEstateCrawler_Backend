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
#     test_listings = [{'link': '/iad/immobilien/d/mietwohnungen/steiermark/graz/schoene-praxisraeume-im-zentrum-von-graz-ab-jaenner-2024-zu-mieten-755134161/', 'title': 'Schoene praxisraeume im zentrum von graz ab jaenner 2024 zu mieten', 'address': {'zip_code': '8020', 'state': 'Steiermark', 'city': 'Lend', 'street': 'Volksgartenstrasse 22', 'district': None}, 'area': 156, 'number_of_rooms': 4, 'additional_info': 'Balkon, Garten', 'price': 190.0}, {'link': '/iad/immobilien/d/mietwohnungen/burgenland/neusiedl-am-see/wohnung-zu-vermieten-754812046/', 'title': 'Wohnung zu vermieten', 'address': {'zip_code': '7131', 'state': 'Burgenland', 'city': 'Halbturn', 'street': 'Parksiedlung', 'district': None}, 'area': 60, 'number_of_rooms': 2, 'additional_info': None, 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/niederoesterreich/hollabrunn/wohnungen-und-geschaeft-zu-vermieten-752906928/', 'title': 'Wohnungen und geschaeft zu vermieten', 'address': {'zip_code': '2070', 'state': 'Niederoesterreich', 'city': 'Retz', 'street': None, 'district': None}, 'area': 270, 'number_of_rooms': None, 'additional_info': None, 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/oberoesterreich/gmunden/-wohnen-am-land-neue-renovierte-160-m-wohnung-in-ehemaliger-landwirtschaft-751563837/', 'title': ' wohnen am land neue renovierte 160 m wohnung in ehemaliger landwirtschaft', 'address': {'zip_code': '4655', 'state': 'Oberoesterreich', 'city': 'Vorchdorf', 'street': None, 'district': None}, 'area': 161, 'number_of_rooms': None, 'additional_info': None, 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/steiermark/graz/schoene-coworking-arbeitsplaetze-zentrum-von-graz-ab-sofort-zu-mieten-751354005/', 'title': 'Schoene coworking arbeitsplaetze zentrum von graz ab sofort zu mieten', 'address': {'zip_code': '8020', 'state': 'Steiermark', 'city': 'Graz', 'street': 'Griesgasse 12', 'district': None}, 'area': 125, 'number_of_rooms': 3, 'additional_info': None, 'price': 150.0}, {'link': '/iad/immobilien/d/mietwohnungen/burgenland/oberwart/wohnung-markt-allhau-neubau-autobahnnaehe-750859202/', 'title': 'Wohnung markt allhau neubau autobahnnaehe', 'address': {'zip_code': '7411', 'state': 'Burgenland', 'city': 'Markt Allhau', 'street': 'Lärchenweg', 'district': None}, 'area': 68, 'number_of_rooms': 3, 'additional_info': 'Balkon', 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/niederoesterreich/horn/wohnung-zu-vermieten-600751325/', 'title': 'Wohnung zu vermieten', 'address': {'zip_code': '3752', 'state': 'Niederoesterreich', 'city': 'Nonnersdorf', 'street': None, 'district': None}, 'area': 100, 'number_of_rooms': 2, 'additional_info': None, 'price': 200.0}, {'link': '/iad/immobilien/d/mietwohnungen/niederoesterreich/waidhofen-an-der-ybbs/wohnung-im-neubau-mit-garten-und-kellerbereich-748880609/', 'title': 'Wohnung im neubau mit garten und kellerbereich', 'address': {'zip_code': '3340', 'state': 'Niederoesterreich', 'city': 'St. Georgen in der Klaus', 'street': 'Dieminger-Siedlung', 'district': None}, 'area': 60, 'number_of_rooms': 2, 'additional_info': 'Garten', 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/oberoesterreich/wels/wohnung-fuer-mitarbeiter-bett-zum-vermieten-748408297/', 'title': 'Wohnung fuer mitarbeiter bett zum vermieten', 'address': {'zip_code': '4600', 'state': 'Oberoesterreich', 'city': 'Wels', 'street': 'Linzerstrasse', 'district': None}, 'area': 75, 'number_of_rooms': 3, 'additional_info': None, 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/niederoesterreich/amstetten/phenthaus-wohnung-neu-in-zentrum-seitenstetten-90-m2-80m-terrasse-zu-vermieten-747294120/', 'title': 'Phenthaus wohnung neu in zentrum seitenstetten 90 m2 80m terrasse zu vermieten', 'address': {'zip_code': '3353', 'state': 'Niederoesterreich', 'city': 'Seitenstetten', 'street': 'Steyrerstrasse 2', 'district': None}, 'area': 90, 'number_of_rooms': None, 'additional_info': None, 'price': 1.0}, {'link': '/iad/immobilien/d/mietwohnungen/oberoesterreich/rohrbach/wohnung-oder-bueroraeumlichkeiten-zu-vermieten-747287423/', 'title': 'Wohnung oder bueroraeumlichkeiten zu vermieten', 'address': {'zip_code': '4152', 'state': 'Oberoesterreich', 'city': 'Sarleinsbach', 'street': 'Am Teichfeld 4/2', 'district': None}, 'area': 137, 'number_of_rooms': 3, 'additional_info': 'Terrasse, Garten', 'price': None}, {'link': '/iad/immobilien/d/mietwohnungen/niederoesterreich/wiener-neustadt/wohnen-in-wiener-neustadt-746042680/', 'title': 'Wohnen in wiener neustadt', 'address': {'zip_code': '2700', 'state': 'Niederoesterreich', 'city': 'Wiener Neustadt', 'street': 'Pöckgasse', 'district': None}, 'area': 87, 'number_of_rooms': 3, 'additional_info': None, 'price': 1.0}]
#     print(format_listings(test_listings))
#
# if __name__ == '__main__':
#     main()
