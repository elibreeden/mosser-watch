import argparse
import logging
from config import get_settings
from ebay import get_ebay_access_token, search_ebay_items
from notifier import format_sms, send_sms
from storage import load_seen_item_ids, save_seen_item_ids, get_new_items

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def run_once(dry_run: bool = False, notify_existing: bool = False) -> None:
    settings = get_settings()

    logging.info("Starting search for query: %s", settings.search_query)

    access_token = get_ebay_access_token(
        settings.ebay_client_id,
        settings.ebay_client_secret,
    )

    items = search_ebay_items(
        access_token=access_token,
        query=settings.search_query,
        marketplace_id=settings.marketplace_id,
        limit=settings.max_results,
        min_price=settings.min_price,
        max_price=settings.max_price,
    )

    logging.info("Found %s listings from eBay.", len(items))

    seen_ids = load_seen_item_ids()

    if notify_existing:
        new_items = items
        logging.info("notify_existing enabled. Treating current results as new.")
    else:
        new_items = get_new_items(items, seen_ids)

    logging.info("Found %s new listings.", len(new_items))

    for item in new_items:
        sms_body = format_sms(item)

        if dry_run:
            print("\n--- DRY RUN SMS ---")
            print(sms_body)
            print("--- END SMS ---\n")
        else:
            sid = send_sms(
                account_sid=settings.twilio_account_sid,
                auth_token=settings.twilio_auth_token,
                from_number=settings.twilio_from_number,
                to_number=settings.to_phone_number,
                body=sms_body,
            )
            logging.info("Sent SMS for item %s. Twilio SID: %s", item["item_id"], sid)

        seen_ids.add(item["item_id"])

    save_seen_item_ids(seen_ids)
    logging.info("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mosser Cat eBay SMS alert bot")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print SMS messages instead of sending them.",
    )
    parser.add_argument(
        "--notify-existing",
        action="store_true",
        help="Treat current search results as new. Useful for testing formatting.",
    )

    args = parser.parse_args()
    run_once(dry_run=args.dry_run, notify_existing=args.notify_existing)
