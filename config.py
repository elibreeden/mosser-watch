from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    ebay_client_id: str
    ebay_client_secret: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    to_phone_number: str
    search_query: str = "Mosser Cat"
    max_results: int = 25
    marketplace_id: str = "EBAY_US"
    max_price: str | None = None
    min_price: str | None = None

def get_settings() -> Settings:
    required = [
        "EBAY_CLIENT_ID",
        "EBAY_CLIENT_SECRET",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_FROM_NUMBER",
        "TO_PHONE_NUMBER",
    ]

    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in your credentials."
        )

    return Settings(
        ebay_client_id=os.environ["EBAY_CLIENT_ID"],
        ebay_client_secret=os.environ["EBAY_CLIENT_SECRET"],
        twilio_account_sid=os.environ["TWILIO_ACCOUNT_SID"],
        twilio_auth_token=os.environ["TWILIO_AUTH_TOKEN"],
        twilio_from_number=os.environ["TWILIO_FROM_NUMBER"],
        to_phone_number=os.environ["TO_PHONE_NUMBER"],
        search_query=os.getenv("SEARCH_QUERY", "Mosser Cat"),
        max_results=int(os.getenv("MAX_RESULTS", "25")),
        marketplace_id=os.getenv("MARKETPLACE_ID", "EBAY_US"),
        max_price=os.getenv("MAX_PRICE") or None,
        min_price=os.getenv("MIN_PRICE") or None,
    )
