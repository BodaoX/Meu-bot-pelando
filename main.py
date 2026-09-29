import time
import hashlib
from datetime import datetime

from db import (
    init_db,
    get_offer,
    insert_offer,
    update_price,
    mark_sent
)
from scraper import fetch_latest_offers
from sender import send_offer

limit = 3
CHECK_INTERVAL = 30

init_db()
print("bot iniciado. monitorando ofertas...")

while True:

    offers = fetch_latest_offers(limit=limit)

    if not offers:
        print("nenhuma oferta encontrada")
        time.sleep(CHECK_INTERVAL)
        continue

    offer = offers[0]
    print(f"oferta encontrada: {offer['title']} | R$ {offer['price']}")

    offer_id = hashlib.md5(
        offer["sourceUrl"].encode()
    ).hexdigest()

    db_offer = get_offer(offer_id)
    should_send = False

    if not db_offer:
        print("oferta nova, salvando no banco")
        insert_offer(offer_id, offer)
        should_send = True
    else:
        _, _, _, _, current_price, last_sent_price, *_ = db_offer

        if offer["price"] != current_price:
            print(f"preço mudou: {current_price} → {offer['price']}")
            update_price(offer_id, offer["price"])

        if last_sent_price is None or offer["price"] < last_sent_price:
            print("preço menor que o último enviado")
            should_send = True
        else:
            print("oferta já enviada anteriormente")

    if should_send:
        payload = {
            "title": offer["title"],
            "price": offer["price"],
            "image_url": offer.get("image", {}).get("url"),
            "source_url": offer["sourceUrl"],
            "coupon_code": offer.get("couponCode") or "❌"
        }

        print("enviando oferta...")

        if send_offer(payload):
            mark_sent(offer_id, offer["price"])
            print("oferta enviada com sucesso")
        else:
            print("falha ao enviar oferta")

    time.sleep(CHECK_INTERVAL)
