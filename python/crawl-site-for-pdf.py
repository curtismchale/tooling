import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Website to scan
BASE_URL = "https://www.cityofsanrafael.org"

# Paths to exclude (e.g., "/admin" will ignore all URLs starting with "http://example.com/admin")
EXCLUDED_PATHS = ["/wp-admin", "/documents", "/#proud-header-*"]

# Number of threads (adjust based on needs)
MAX_THREADS = 10

VISITED_PAGES = set()  # Track visited pages
CSV_FILE = "pdf_links.csv"  # Output file

# Create CSV file and write header at the beginning
with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page URL", "PDF File URL"])


def get_all_links(url):
    """Fetch all links from a given page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all links
        return [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    except requests.RequestException:
        return []


def is_same_domain(url):
    """Check if the URL belongs to the same domain."""
    return urlparse(url).netloc == urlparse(BASE_URL).netloc


def is_excluded(url):
    """Check if a URL should be excluded based on the blocked paths."""
    parsed_url = urlparse(url)
    for path in EXCLUDED_PATHS:
        if parsed_url.path.startswith(path):
            return True  # This URL is in an excluded path
    return False


def crawl_website(url):
    """Crawl the website, find PDFs, and save results while skipping excluded paths."""
    if url in VISITED_PAGES or not is_same_domain(url) or is_excluded(url):
        return []  # Skip if already visited, different domain, or excluded path

    print(f"📂 Crawling: {url}")  # Live progress update
    VISITED_PAGES.add(url)  # Mark page as visited
    found_links = []  # To store discovered links

    # Get all links on the current page
    links = get_all_links(url)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for link in links:
            if link.endswith(".pdf"):  # Found a PDF
                print(f"✅ Found PDF: {link}")
                writer.writerow([url, link])  # Write directly to CSV
            elif link not in VISITED_PAGES:  # New page to crawl
                found_links.append(link)  # Collect new pages to scan

    return found_links


# Multi-threaded crawling using a dynamic queue
def threaded_crawl():
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {executor.submit(crawl_website, BASE_URL): BASE_URL}  # Start with BASE_URL

        while future_to_url:
            for future in as_completed(future_to_url):
                new_urls = future.result()  # Get new URLs found on the page
                del future_to_url[future]  # Remove completed task

                # Submit new pages to the executor
                for new_url in new_urls:
                    if new_url not in VISITED_PAGES:
                        future_to_url[executor.submit(crawl_website, new_url)] = new_url


# Start multi-threaded crawling
print("🔍 Starting deep scan with multi-threading...\n")
threaded_crawl()
print("\n✅ Scan complete! PDF results saved in pdf_links.csv 🎉")
