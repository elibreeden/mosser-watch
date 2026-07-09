import smtplib
from email.message import EmailMessage

from twilio.rest import Client


def format_sms(item: dict) -> str:
    price = "Price unavailable"
    if item.get("price_value") and item.get("price_currency"):
        price = f"{item['price_value']} {item['price_currency']}"

    buying_options = ", ".join(item.get("buying_options") or [])
    if buying_options:
        buying_options = f"\nType: {buying_options}"

    condition = item.get("condition")
    condition_line = f"\nCondition: {condition}" if condition else ""

    seller = item.get("seller_username")
    seller_line = f"\nSeller: {seller}" if seller else ""

    return (
        "🐈 New Mosser Cat listing!\n"
        f"{item.get('title', 'Untitled listing')}\n"
        f"{price}"
        f"{buying_options}"
        f"{condition_line}"
        f"{seller_line}\n"
        f"{item.get('item_web_url', '')}"
    )


def send_sms(
    account_sid: str,
    auth_token: str,
    from_number: str,
    to_number: str,
    body: str,
) -> str:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
    )

    return message.sid


def send_email(
    from_email: str,
    app_password: str,
    to_email: str,
    subject: str,
    body: str,
) -> None:
    """
    Send a notification email using Gmail.
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)