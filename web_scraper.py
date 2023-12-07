import csv
import requests
from urllib.parse import urlparse
from tqdm import tqdm
from bs4 import BeautifulSoup
import xmltodict

# Function to check if a URL is internal
def is_internal_url(main_domain, url):
    return urlparse(url).netloc == main_domain

# Function to extract title and meta description from a URL
def extract_title_and_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else 'No title found'
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description_tag['content'] if meta_description_tag else 'No meta description found'
        return title, meta_description
    except Exception as e:
        return f"Error: {e}", None

def scrape_internal_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        sitemap_dict = xmltodict.parse(response.content)

        # Extract and filter internal URLs from the sitemap
        main_domain = urlparse(sitemap_url).netloc
        sitemap_urls = sitemap_dict.get('sitemapindex', {}).get('sitemap', [])

        print(f"\nWorking on main sitemap: {sitemap_url}")

        internal_urls = []
        if not sitemap_urls:  # If no sub-sitemaps, directly scrape URLs from the main sitemap
            urls = sitemap_dict.get('urlset', {}).get('url', [])
            internal_urls = [url['loc'] for url in urls if is_internal_url(main_domain, url['loc'])]
            
        else:
            for sitemap_url_info in tqdm(sitemap_urls, desc="Processing Sub-Sitemaps", unit=" Sub-Sitemap"):
                sub_sitemap_url = sitemap_url_info.get('loc')

                try:
                    sub_sitemap_response = requests.get(sub_sitemap_url)
                    sub_sitemap_response.raise_for_status()

                    sub_sitemap_dict = xmltodict.parse(sub_sitemap_response.content)
                    urls = sub_sitemap_dict.get('urlset', {}).get('url', [])

                    sub_sitemap_internal_urls = []
                    if isinstance(urls, list):
                        for url in urls:
                            if is_internal_url(main_domain, url['loc']):
                                sub_sitemap_internal_urls.append(url['loc'])
                    elif isinstance(urls, dict):
                        if is_internal_url(main_domain, urls.get('loc')):
                            sub_sitemap_internal_urls.append(urls['loc'])

                    internal_urls.extend(sub_sitemap_internal_urls)
                except Exception as e:
                    print(f"Error scraping internal URLs from sub-sitemap {sub_sitemap_url}: {e}")

        return internal_urls

    except Exception as e:
        print(f"Error scraping internal URLs from main sitemap: {e}")
        return []

# Function to process internal URLs and write results to CSV
def process_and_write_to_csv(internal_urls):
    if not internal_urls:
        print("No internal URLs found.")
        return

    # Process URLs and write results to CSV
    output_csv_file = 'output_results.csv'
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['URL', 'Title', 'Meta Description'])  # Header row

        for url in tqdm(internal_urls, desc="Processing URLs", unit="URL"):
            title, meta_description = extract_title_and_description(url)
            csv_writer.writerow([url, title, meta_description])

    print(f"\nResults written to {output_csv_file}")

if __name__ == "__main__":
    # Interactive input
    website_url = input("Enter the URL of the main sitemap.xml to scrape: ").strip()

    # Check if the provided URL ends with "sitemap.xml"
    if website_url.endswith("sitemap.xml"):
        # Scrape internal URLs from the main sitemap
        main_internal_urls = scrape_internal_urls_from_sitemap(website_url)

        # Process and write results for all internal URLs
        process_and_write_to_csv(main_internal_urls)
    else:
        print("Invalid URL. Please provide a valid main sitemap URL.")