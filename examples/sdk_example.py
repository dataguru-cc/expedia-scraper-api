"""Expedia scraper API: DataGuru Python SDK example.

Runs DataGuru's Expedia APIs and prints the JSON they return:
  - Expedia Hotel Details: $0.0022 per successful request ($2.20 per 1,000)
  - Expedia Hotel Search: $0.02 per successful request ($20.00 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py expedia-hotel-details
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def expedia_hotel_details(dg):
    """Expedia Hotel Details: Get an Expedia property from its URL, including star rating, address and coordinates, guest rating and review count, description, amenities by category, policies and fees, nearby places, FAQs and photos."""
    return dg.call(
        "expedia-hotel-details",
        hotel_url="https://www.expedia.com/Paris-Hotels-Novotel-Paris-Centre-Bercy.h9732.Hotel-Information",
    )


def expedia_hotel_search(dg):
    """Expedia Hotel Search: Search Expedia for a destination and stay dates and get matching properties with nightly and total prices, guest ratings, review counts, neighborhoods, amenity highlights, refund options and photos."""
    return dg.call(
        "expedia-hotel-search",
        query="Singapore",
    )


EXAMPLES = {
    "expedia-hotel-details": expedia_hotel_details,
    "expedia-hotel-search": expedia_hotel_search,
}
DEFAULT = ['expedia-hotel-details', 'expedia-hotel-search']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
