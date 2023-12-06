# SEO Sitemap URL Scraper

This tool allows users to scrape all URLs from multi-level sitemaps. It uses BeautifulSoup to grab Meta Descriptions and Titles from the pages and exports it to a CSV.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/K1N6Y/SitemapScraper
    ```

2. Navigate to the project directory:

    ```bash
    cd sitemapscraper
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the tool, follow these steps:

1. Run the script:

    ```bash
    python web_scraper.py
    ```

2. Enter the URL of the main sitemap.xml when prompted.

3. The tool will scrape all URLs from the sitemap, grab the titles and meta descriptions, and export the results to a CSV file.

## Contributing

If you would like to contribute to the project, feel free to fork and submit a pull request.

## Dependencies

- beautifulsoup4==4.10.0
- requests==2.26.0
- tqdm==4.62.3
- xmltodict==0.12.0
