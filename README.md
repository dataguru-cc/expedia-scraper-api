# Expedia Scraper API

Scrape Expedia with a JSON API. This repo has working Python examples for DataGuru's Expedia scraper APIs: Expedia Hotel Details and Expedia Hotel Search.

[DataGuru](https://dataguru.cc) runs the scraping, proxies, retries and parsing, and returns clean JSON. You pay only for successful requests, from $0.0022 per request, out of a prepaid balance: no subscription. New accounts get $1.00 of free credit.

## Expedia APIs

| API | What it returns | Price | Page |
| --- | --- | --- | --- |
| [Expedia Hotel Details](#expedia-hotel-details) | Get an Expedia property from its URL, including star rating, address and coordinates, guest rating and review count, description, amenities by category, policies and fees, nearby places, FAQs and photos. | $0.0022 | [https://dataguru.cc/apis/expedia-hotel-details/](https://dataguru.cc/apis/expedia-hotel-details/) |
| [Expedia Hotel Search](#expedia-hotel-search) | Search Expedia for a destination and stay dates and get matching properties with nightly and total prices, guest ratings, review counts, neighborhoods, amenity highlights, refund options and photos. | $0.02 | [https://dataguru.cc/apis/expedia-hotel-search/](https://dataguru.cc/apis/expedia-hotel-search/) |

## Quick start

1. Create a free account and an API key at [dashboard.dataguru.cc](https://dashboard.dataguru.cc).
2. Install and run:

```bash
git clone https://github.com/dataguru-cc/expedia-scraper-api.git
cd expedia-scraper-api
pip install -r requirements.txt
export DATAGURU_API_KEY="your key"
python examples/sdk_example.py expedia-hotel-details
```

## Examples

Every example covers all 2 Expedia APIs. Pass an API name to run just one; with no name each script runs them all, and each call is billed at the price above.

| File | Style | Run |
| --- | --- | --- |
| [`examples/sdk_example.py`](examples/sdk_example.py) | [DataGuru Python SDK](https://github.com/dataguru-cc/dataguru-python) (`pip install dataguru-sdk`), one function per API, saves JSON to `output/` | `python examples/sdk_example.py` |
| [`examples/requests_example.py`](examples/requests_example.py) | Plain `requests`, synchronous | `python examples/requests_example.py` |
| [`examples/async_example.py`](examples/async_example.py) | `asyncio` + `httpx`, concurrent with a limit | `python examples/async_example.py` |
| [`examples/scrapy_spider.py`](examples/scrapy_spider.py) | Scrapy spider, items to JSON/CSV | `scrapy runspider examples/scrapy_spider.py -O expedia.json` |

All requests use the header `Authorization: Api-Key YOUR_API_KEY`. Errors return `{"success": false, "error": {"code", "message", "request_id"}}`, with HTTP 402 when the balance runs out and 429 (with `Retry-After`) when rate limited. Failed requests are not charged.

## API reference

### Expedia Hotel Details

Get an Expedia property from its URL, including star rating, address and coordinates, guest rating and review count, description, amenities by category, policies and fees, nearby places, FAQs and photos.

- Endpoint: `POST https://api.dataguru.cc/api/v1/expedia/hotels/details`
- Price: $0.0022 per successful request ($2.20 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/expedia-hotel-details/
- Documentation: https://dataguru.cc/documentation/expedia-hotel-details/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `hotel_url` | string | yes | Full Expedia hotel URL (e.g. https://www.expedia.com/Paris-Hotels-Novotel-Paris-Centre-Bercy.h9732.Hotel-Information). |
| `location` | string | no | Two-letter country code to fetch the page from (default US). |

**Response fields:** `hotel_id`, `name`, `url`, `star_rating`, `address`, `latitude`, `longitude`, `rating`, `tagline`, `description`, `about`, `amenities`, `policies`, `important_information`, `location`, `faqs`, `photo_count`, `photo_categories`, `photos`, `time_taken`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/expedia/hotels/details" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hotel_url": "https://www.expedia.com/Paris-Hotels-Novotel-Paris-Centre-Bercy.h9732.Hotel-Information"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "hotel_id": "1234567890",
  "name": "string",
  "url": "https://example.com/...",
  "star_rating": 0.0,
  "address": {
    "full": "string",
    "street": "string",
    "city": "string",
    "region": "string",
    "postal_code": "string",
    "country": "string"
  },
  "latitude": 0.0,
  "longitude": 0.0,
  "rating": {
    "score": 0.0,
    "score_max": 0,
    "word": "string",
    "count": 0
  },
  "tagline": "string",
  "description": "string",
  "about": [
    "string"
  ],
  "amenities": [
    {
      "scope": "string",
      "category": "string",
      "items": [
        "string"
      ]
    }
  ],
  "policies": [
    {
      "title": "string",
      "items": [
        "string"
      ]
    }
  ],
  "important_information": [
    {
      "title": "string",
      "items": [
        "string"
      ]
    }
  ],
  "location": {
    "neighborhood_description": "string",
    "area": "string",
    "nearby": [
      {
        "name": "string",
        "distance": "string",
        "travel_time": "string"
      }
    ]
  },
  "faqs": [
    {
      "question": "string",
      "answer": "string"
    }
  ],
  "photo_count": 0,
  "photo_categories": [
    {
      "name": "string",
      "count": 0
    }
  ],
  "photos": [
    {
      "url": "https://example.com/...",
      "thumbnail": "string",
      "description": "string"
    }
  ],
  "time_taken": 0.0,
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Expedia Hotel Details",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### Expedia Hotel Search

Search Expedia for a destination and stay dates and get matching properties with nightly and total prices, guest ratings, review counts, neighborhoods, amenity highlights, refund options and photos.

- Endpoint: `POST https://api.dataguru.cc/api/v1/expedia/hotels/search`
- Price: $0.02 per successful request ($20.00 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/expedia-hotel-search/
- Documentation: https://dataguru.cc/documentation/expedia-hotel-search/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `adults` | integer | no | Number of adult guests in one room (default 2). |
| `checkin` | string | no | Check-in date (YYYY-MM-DD). Defaults to 14 days from today. |
| `checkout` | string | no | Checkout date (YYYY-MM-DD). Defaults to one night after check-in; stays up to 28 nights. |
| `limit` | integer | no | Maximum number of properties to return (1-100). Default: `50`. |
| `location` | string | no | Two-letter country code to search from (default US). |
| `query` | string | yes | Destination to search, e.g. "Singapore", "Paris, France" or "Times Square, New York". |

**Response fields:** `search_parameters`, `destination`, `heading`, `results_summary`, `total_results`, `returned_results`, `time_taken`, `properties`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/expedia/hotels/search" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Singapore"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "search_parameters": {
    "query": "string",
    "checkin": "string",
    "checkout": "string",
    "nights": 0,
    "adults": 0,
    "location": "string",
    "limit": 0,
    "url": "https://example.com/..."
  },
  "destination": {
    "name": "string",
    "region_id": "1234567890"
  },
  "heading": "string",
  "results_summary": "string",
  "total_results": 0,
  "returned_results": 0,
  "time_taken": 0.0,
  "properties": [
    {
      "position": 0,
      "hotel_id": "1234567890",
      "name": "string",
      "url": "https://example.com/...",
      "neighborhood": "string",
      "review_score": 0.0,
      "review_score_max": 0,
      "review_score_word": "string",
      "review_count": 0,
      "summary": "string",
      "amenities": [
        "string"
      ],
      "price": {
        "per_night": 0.0,
        "per_night_formatted": "string",
        "total": 0.0,
        "total_formatted": "string",
        "original_total": 0.0,
        "original_total_formatted": "string",
        "discount": "string",
        "currency": "USD",
        "taxes_and_fees_included": false,
        "messages": [
          "string"
        ]
      },
      "rooms_left": 0,
      "refund_options": [
        "string"
      ],
      "badges": [
        "string"
      ],
      "sponsored": false,
      "photos": [
        "string"
      ]
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Expedia Hotel Search",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

## More

- Python SDK and examples for all DataGuru APIs: [github.com/dataguru-cc/dataguru-python](https://github.com/dataguru-cc/dataguru-python) ([docs](https://dataguru-python.readthedocs.io/))
- Every API, with a live playground: [https://dataguru.cc/apis/](https://dataguru.cc/apis/)
- Use DataGuru from Claude, ChatGPT or Cursor through the MCP server: [https://dataguru.cc/mcp/](https://dataguru.cc/mcp/)
- Run thousands of inputs from a CSV at half price with batch jobs: [https://dataguru.cc/documentation/](https://dataguru.cc/documentation/)
- Other scraper APIs: [1688](https://github.com/dataguru-cc/1688-scraper-api), [Airbnb](https://github.com/dataguru-cc/airbnb-scraper-api), [Alibaba](https://github.com/dataguru-cc/alibaba-scraper-api), [AliExpress](https://github.com/dataguru-cc/aliexpress-scraper-api), [Amazon](https://github.com/dataguru-cc/amazon-scraper-api), [arXiv](https://github.com/dataguru-cc/arxiv-scraper-api), [ASOS](https://github.com/dataguru-cc/asos-scraper-api), [Best Buy](https://github.com/dataguru-cc/best-buy-scraper-api), [Booking.com](https://github.com/dataguru-cc/booking-scraper-api), [Brave Search](https://github.com/dataguru-cc/brave-search-scraper-api), [CA State Bar](https://github.com/dataguru-cc/california-state-bar-scraper-api), [Capterra](https://github.com/dataguru-cc/capterra-scraper-api), [CoinGecko](https://github.com/dataguru-cc/coingecko-scraper-api), [CoinMarketCap](https://github.com/dataguru-cc/coinmarketcap-scraper-api), [Companies House](https://github.com/dataguru-cc/companies-house-scraper-api), [Costco](https://github.com/dataguru-cc/costco-scraper-api), [CourtListener](https://github.com/dataguru-cc/courtlistener-scraper-api), [Crunchbase](https://github.com/dataguru-cc/crunchbase-scraper-api), [Discord](https://github.com/dataguru-cc/discord-scraper-api), [DoorDash](https://github.com/dataguru-cc/doordash-scraper-api), [eBay](https://github.com/dataguru-cc/ebay-scraper-api), [Etsy](https://github.com/dataguru-cc/etsy-scraper-api), [Fiverr](https://github.com/dataguru-cc/fiverr-scraper-api), [Flipkart](https://github.com/dataguru-cc/flipkart-scraper-api), [Glassdoor](https://github.com/dataguru-cc/glassdoor-scraper-api), [Google Flights](https://github.com/dataguru-cc/google-flights-scraper-api), [Google Patents](https://github.com/dataguru-cc/google-patents-scraper-api), [Google Scholar](https://github.com/dataguru-cc/google-scholar-scraper-api), [Google Search](https://github.com/dataguru-cc/google-search-scraper-api), [Grubhub](https://github.com/dataguru-cc/grubhub-scraper-api), [Home Depot](https://github.com/dataguru-cc/home-depot-scraper-api), [Instagram](https://github.com/dataguru-cc/instagram-scraper-api), [Investing.com](https://github.com/dataguru-cc/investing-com-scraper-api), [Justia](https://github.com/dataguru-cc/justia-scraper-api), [Kayak](https://github.com/dataguru-cc/kayak-scraper-api), [Kick](https://github.com/dataguru-cc/kick-scraper-api), [Lazada](https://github.com/dataguru-cc/lazada-scraper-api), [MarketWatch](https://github.com/dataguru-cc/marketwatch-scraper-api), [Mercado Libre](https://github.com/dataguru-cc/mercado-libre-scraper-api), [Monster](https://github.com/dataguru-cc/monster-scraper-api), [OpenCorporates](https://github.com/dataguru-cc/opencorporates-scraper-api), [OpenTable](https://github.com/dataguru-cc/opentable-scraper-api), [PACER](https://github.com/dataguru-cc/pacer-scraper-api), [PitchBook](https://github.com/dataguru-cc/pitchbook-scraper-api), [PubMed](https://github.com/dataguru-cc/pubmed-scraper-api), [Reddit](https://github.com/dataguru-cc/reddit-scraper-api), [Redfin](https://github.com/dataguru-cc/redfin-scraper-api), [Resy](https://github.com/dataguru-cc/resy-scraper-api), [Rightmove](https://github.com/dataguru-cc/rightmove-scraper-api), [SEC EDGAR](https://github.com/dataguru-cc/sec-edgar-scraper-api), [Seeking Alpha](https://github.com/dataguru-cc/seeking-alpha-scraper-api), [Shopee](https://github.com/dataguru-cc/shopee-scraper-api), [Skyscanner](https://github.com/dataguru-cc/skyscanner-scraper-api), [Target](https://github.com/dataguru-cc/target-scraper-api), [TikTok](https://github.com/dataguru-cc/tiktok-scraper-api), [TradingView](https://github.com/dataguru-cc/tradingview-scraper-api), [TripAdvisor](https://github.com/dataguru-cc/tripadvisor-scraper-api), [Trulia](https://github.com/dataguru-cc/trulia-scraper-api), [TrustRadius](https://github.com/dataguru-cc/trustradius-scraper-api), [Twitch](https://github.com/dataguru-cc/twitch-scraper-api), [Uber Eats](https://github.com/dataguru-cc/uber-eats-scraper-api), [Upwork](https://github.com/dataguru-cc/upwork-scraper-api), [Vrbo](https://github.com/dataguru-cc/vrbo-scraper-api), [Walmart](https://github.com/dataguru-cc/walmart-scraper-api), [Wayfair](https://github.com/dataguru-cc/wayfair-scraper-api), [X (Twitter)](https://github.com/dataguru-cc/twitter-scraper-api), [Yahoo Finance](https://github.com/dataguru-cc/yahoo-finance-scraper-api), [YouTube](https://github.com/dataguru-cc/youtube-scraper-api), [Zillow](https://github.com/dataguru-cc/zillow-scraper-api), [ZoomInfo](https://github.com/dataguru-cc/zoominfo-scraper-api), [Zoopla](https://github.com/dataguru-cc/zoopla-scraper-api)

## License

The example code is MIT licensed. Use of the DataGuru API is subject to the [terms of service](https://dataguru.cc/terms/).
