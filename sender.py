import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1554468166845857853/CXWoA6aYUOLLilxQjNASQHPJPCtAlUwDSn9zcgwdViV6M_mXreTqIcFQqC8nxA7jvQWS"


def format_price_br(value: float) -> str:
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def send_offer(payload: dict) -> bool:
    embed = {
        "title": payload["title"],
        "url": payload["source_url"],
        "color": 0x2ECC71,
        "timestamp": datetime.utcnow().isoformat(),
        "fields": [
            {
                "name": "Preço",
                "value": f"R$ {format_price_br(payload['price'])}",
                "inline": True
            },
            {
                "name": "Cupom",
                "value": payload["coupon_code"],
                "inline": True
            }
        ]
    }

    if payload.get("image_url"):
        embed["image"] = {"url": payload["image_url"]}

    data = {
        "username": "sonic me diga aonde fica o h em chorinthiahns",
        "embeds": [embed]
    }

    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
        return r.status_code in (200, 204)
    except Exception as e:
        print("[sender] erro ao enviar webhook:", e)
        return False
