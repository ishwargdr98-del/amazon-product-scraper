amazon-product-scraper

 🛍️ Amazon Product Scraper (Playwright + Python)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Fast%20Scraping-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

A high-speed Amazon product scraper built with Playwright that extracts:
- ✅ Product Title  
- ✅ Price  
- ✅ Rating  
- ✅ Product Link (absolute URLs)

Perfect for research, analysis, or price-tracking automation.

---

⚙️ Features
- 🚀 Super Fast — Uses Playwright with resource blocking (no images/fonts)
- 🧠 Smart Selectors — Auto-detects multiple title formats
- 🔗 Full Product Links — Converts ASINs into working URLs
- 📊 Excel Export — Clean, ready-to-use `.xlsx` file output
- 🧩 Lightweight — No complex setup, pure Python

---

📦 Installation

1️⃣ Clone this repository:
```bash
git clone https://github.com/ishwargdr98-del/amazon-product-scraper.git
cd amazon-product-scraper

2️⃣ Install required packages:

pip install -r requirements.txt


3️⃣ Install Playwright browsers (first time only):

playwright install

🚀 Usage

Run the scraper:

python Scraping.py


Then enter any product keyword, e.g.:

Enter product keyword (e.g., shoes, smartphones): shoes


✅ Output:

Data automatically saved to Excel file:

amazon_data_YYYYMMDD_HHMMSS.xlsx


🧠 Example Output (Excel)
Title	Price	Rating	Link
Nike Running Shoes	3499	4.5 out of 5 stars	https://www.amazon.in/dp/B0XYZ1234

...	...	...	...


⚠️ Disclaimer

This tool is for educational and research purposes only.
Scraping Amazon pages may violate their Terms of Service — use responsibly.

🧑‍💻 Author

Ishwar Bhardwaj
📧 github.com/ishwargdr98-del

💡 Passionate about automation, AI, and practical tech tools.

Support

If you like this project,
give it a star ⭐ on GitHub!

