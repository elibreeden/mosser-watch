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
