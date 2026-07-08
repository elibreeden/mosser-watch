import base64
import requests
from typing import Any

EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

def get_ebay_access_token(client_id: str, client_secret: str) -> str:
    """
    Gets an OAuth access token using eBay's client credentials flow.

    This token is used to call the Browse API.
    """
    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=data, timeout=20)
    response.raise_for_status()

    return response.json()["access_token"]

def search_ebay_items(
    access_token: str,
    query: str,
    marketplace_id: str = "EBAY_US",
    limit: int = 25,
    min_price: str | None = None,
    max_price: str | None = None,
) -> list[dict[str, Any]]:
    """
    Searches eBay Browse API for active listings.

    Returns normalized item dictionaries so the rest of the app does not depend
    on the full eBay response shape.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-EBAY-C-MARKETPLACE-ID": marketplace_id,
    }

    params: dict[str, Any] = {
        "q": query,
        "limit": limit,
        "sort": "newlyListed",
    }

    filters = []
    if min_price:
        filters.append(f"price:[{min_price}..]")
    if max_price:
        filters.append(f"price:[..{max_price}]")
    if filters:
        params["filter"] = ",".join(filters)

    response = requests.get(EBAY_SEARCH_URL, headers=headers, params=params, timeout=20)
    response.raise_for_status()

    payload = response.json()
    raw_items = payload.get("itemSummaries", [])

    return [normalize_item(item) for item in raw_items]

def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    price = item.get("price") or {}
    shipping = item.get("shippingOptions", [{}])[0].get("shippingCost", {}) if item.get("shippingOptions") else {}

    return {
        "item_id": item.get("itemId"),
        "title": item.get("title", "Untitled listing"),
        "price_value": price.get("value"),
        "price_currency": price.get("currency"),
        "shipping_value": shipping.get("value"),
        "condition": item.get("condition"),
        "seller_username": (item.get("seller") or {}).get("username"),
        "item_web_url": item.get("itemWebUrl"),
        "image_url": (item.get("image") or {}).get("imageUrl"),
        "buying_options": item.get("buyingOptions", []),
    }
