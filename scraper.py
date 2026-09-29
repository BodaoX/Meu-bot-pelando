import json
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.pelando.com.br"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

def normalize_text(text: str) -> str:
    if not text:
        return text

    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def extract_clean_text(tag):
    if not tag:
        return ""

    parts = [t.strip() for t in tag.stripped_strings]
    return parts[0] if parts else ""


def fetch_latest_offers(limit=5):
    print("[scraper] buscando ofertas...")

    r = requests.get(f"{BASE_URL}/recentes", headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    script = soup.find("script", id="feed-schema")
    if not script:
        print("[scraper] feed-schema não encontrado")
        return []

    data = json.loads(script.string)
    parts = data.get("mainEntity", {}).get("hasPart", [])

    offers = []

    for part in parts[:limit]:
        url = part.get("url")
        if not url:
            continue

        offer = fetch_offer_details(url)
        if offer:
            offers.append(offer)

    print(f"[scraper] {len(offers)} ofertas encontradas")
    return offers


def fetch_offer_details(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None

    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.find("h1")
    raw_title = extract_clean_text(title_tag)
    title = normalize_text(raw_title)

    text = soup.get_text(separator=" ", strip=True)

    price_match = re.search(r"R\$\s?[\d\.]+(?:,\d{2})?", text)
    if price_match:
        price = float(
            price_match.group()
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
    else:
        price = 0.0

    image = soup.find("meta", property="og:image")
    image_url = image["content"] if image else None

    coupon = None
    coupon_el = soup.find(string=re.compile(r"cupom", re.I))
    if coupon_el:
        coupon = normalize_text(coupon_el.strip())

    return {
        "title": title,
        "price": price,
        "sourceUrl": url,
        "image": {"url": image_url},
        "couponCode": coupon
    }
