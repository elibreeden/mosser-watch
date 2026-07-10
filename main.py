import argparse
import logging
import time

from config import get_settings
from ebay import get_ebay_access_token, search_ebay_items
from notifier import format_sms, send_sms, send_email
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

    logging.info("Checked eBay. Found %s listings.", len(items))

    if items:
        logging.info("Newest returned item: %s", items[0].get("title"))

    seen_ids = load_seen_item_ids()

    if notify_existing:
        new_items = items
        logging.info("notify_existing enabled. Treating current results as new.")
    else:
        new_items = get_new_items(items, seen_ids)

    logging.info("Found %s new listings.", len(new_items))

    for item in new_items:
        message_body = format_sms(item)

        if dry_run:
            print("\n--- DRY RUN MESSAGE ---")
            print(message_body)
            print("--- END MESSAGE ---\n")

        else:
            if (
                settings.email_from
                and settings.email_to
                and settings.email_app_password
            ):
                send_email(
                    from_email=settings.email_from,
                    app_password=settings.email_app_password,
                    to_email=settings.email_to,
                    subject="🐈 New Mosser Watch Listing!",
                    body=message_body,
                )
                logging.info("Email sent for item %s.", item["item_id"])

            if (
                settings.twilio_account_sid
                and settings.twilio_auth_token
                and settings.twilio_from_number
                and settings.to_phone_number
            ):
                sid = send_sms(
                    account_sid=settings.twilio_account_sid,
                    auth_token=settings.twilio_auth_token,
                    from_number=settings.twilio_from_number,
                    to_number=settings.to_phone_number,
                    body=message_body,
                )
                logging.info("SMS sent for item %s. SID: %s", item["item_id"], sid)

        seen_ids.add(item["item_id"])

    save_seen_item_ids(seen_ids)

    if new_items:
        logging.info("Sent notifications for %s new listing(s).", len(new_items))
    else:
        logging.info("No new listings.")


def run_watch_mode(
    interval_seconds: int,
    dry_run: bool = False,
    notify_existing: bool = False,
) -> None:
    logging.info(
        "Mosser Watch started. Checking every %s seconds.",
        interval_seconds,
    )

    cycle_count = 0

    while True:
        cycle_count += 1

        try:
            run_once(
                dry_run=dry_run,
                notify_existing=notify_existing,
            )

            if cycle_count % 20 == 0:
                logging.info(
                    "Mosser Watch is still running. Completed %s checks.",
                    cycle_count,
                )

        except Exception:
            logging.exception("Unexpected error during watch cycle.")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mosser Watch eBay alert bot")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print messages instead of sending them.",
    )

    parser.add_argument(
        "--notify-existing",
        action="store_true",
        help="Treat current search results as new. Useful for testing.",
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Keep running and check repeatedly.",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between checks in watch mode.",
    )

    args = parser.parse_args()

    try:
        if args.watch:
            run_watch_mode(
                interval_seconds=args.interval,
                dry_run=args.dry_run,
                notify_existing=args.notify_existing,
            )
        else:
            run_once(
                dry_run=args.dry_run,
                notify_existing=args.notify_existing,
            )

    except KeyboardInterrupt:
        logging.info("Stopped by user.")