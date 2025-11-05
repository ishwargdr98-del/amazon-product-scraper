import pandas as pd
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from datetime import datetime

BASE = "https://www.amazon.in"
DP = "https://www.amazon.in/dp/"

BLOCKED_RESOURCE_TYPES = {"image", "stylesheet", "font"}
BLOCKED_URL_PARTS = (
    "google-analytics", "doubleclick", "adsystem", "adservice",
    "gstatic", "facebook", "bing.com", "beacon", "optimizely"
)

def scrape_amazon_fixed(keyword, pages=2):
    ua = UserAgent()
    rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=ua.random,
            viewport={"width": 1366, "height": 850},
            locale="en-IN"
        )

        # Block heavy requests
        def route_blocker(route, request):
            if request.resource_type in BLOCKED_RESOURCE_TYPES:
                return route.abort()
            if any(part in request.url.lower() for part in BLOCKED_URL_PARTS):
                return route.abort()
            return route.continue_()
        context.route("**/*", route_blocker)

        page = context.new_page()
        page.set_default_timeout(30000)

        for pg in range(1, pages + 1):
            url = f"{BASE}/s?k={keyword.replace(' ', '+')}&page={pg}"
            print(f"\n🔹 Scraping page {pg} -> {url}")
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector('div[data-component-type="s-search-result"]', state="attached")

            # ✅ JavaScript से पूरा data एकसाथ निकालो
            data = page.evaluate("""(dpBase) => {
                const cards = Array.from(document.querySelectorAll('div[data-component-type="s-search-result"]'));
                return cards.map(c => {
                    const asin = c.getAttribute('data-asin') || "";
                    // Title के लिए multiple fallbacks
                    let title = c.querySelector('h2 a span')?.textContent?.trim()
                             || c.querySelector('h2 span')?.textContent?.trim()
                             || c.querySelector('span.a-size-medium.a-color-base.a-text-normal')?.textContent?.trim()
                             || c.querySelector('img.s-image')?.getAttribute('alt')?.trim()
                             || "N/A";

                    // Prefer href; fallback to ASIN
                    let href = c.querySelector('h2 a')?.href || "";
                    if (!href && asin) href = dpBase + asin;

                    const priceWhole = c.querySelector(".a-price .a-price-whole")?.textContent?.replace(/[^\d]/g,'') || "";
                    const priceFrac  = c.querySelector(".a-price .a-price-fraction")?.textContent?.replace(/[^\d]/g,'') || "";
                    const price = priceWhole ? (priceWhole + (priceFrac ? "." + priceFrac : "")) : "N/A";

                    const rating = c.querySelector("span.a-icon-alt")?.textContent?.trim() || "N/A";

                    return { Title: title || "N/A", Price: price, Rating: rating, Link: href || "N/A" };
                });
            }""", DP)

            # ✅ Relative links को absolute बनाओ
            for d in data:
                if d["Link"].startswith("/"):
                    d["Link"] = urljoin(BASE, d["Link"])
            rows.extend(data)

        browser.close()

    return rows


if __name__ == "__main__":
    kw = input("Enter product keyword (e.g., shoes, smartphones): ")
    data = scrape_amazon_fixed(kw, pages=2)
    df = pd.DataFrame(data)
    filename = f"amazon_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n✅ Saved {len(df)} products to '{filename}'")
