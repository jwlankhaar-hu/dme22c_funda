"""Retrieves the house prices from Funda and write them to file."""

import csv
import http
from pathlib import Path

import bs4
import requests

from settings import settings

HEADERS = settings.request_headers
CSV_OPTIONS = settings.csv_options
COLUMN_HEADERS = ['Address', 'Price (euro)']


def export_prices(base_url: str, csv_file: Path) -> None:
    """Get the prices from the URL and write the price list to a CSV 
    file.
    """
    page_urls = construct_page_urls(base_url)
    houses = search(page_urls)
    price_list = [price_row(html) for html in houses]    
    with open(csv_file, 'wt', encoding='utf8') as f:
        writer = csv.writer(f, **CSV_OPTIONS)
        writer.writerow(COLUMN_HEADERS)
        writer.writerows(price_list)        


def get_html(url: str) -> bs4.BeautifulSoup:
    """Request the HTML from the URL and parse it as BeautifulSoup."""
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == http.HTTPStatus.OK:
        html = bs4.BeautifulSoup(resp.content, 'html.parser')
    else:
        html = bs4.BeautifulSoup('', 'html.parser')
    return html


def construct_page_urls(base_url) -> list[str]:
    """Construct all page URLs for the search results."""
    html = get_html(base_url)
    page_links = html.select('a[data-pagination-page]')
    num_of_pages = max(int(a['data-pagination-page']) 
                       for a in page_links)
    page_urls = [f'{base_url}/p{i}' for i in range(1, num_of_pages+1)]
    return page_urls


def search(page_urls: list[str]):
    """Return a list with chunks of the HTML for each house."""
    search_results = []
    for url in page_urls:
        html = get_html(url)
        search_results.extend(html.find_all('li', class_='search-result'))
    return search_results


def price_row(house_html: bs4.BeautifulSoup):
    """Return a tuple with the cleaned address and the price of a 
    house.
    """
    address = parse_address(house_html)
    price = parse_price(house_html)
    return (address, price)


def parse_address(house_html: bs4.BeautifulSoup) -> str:
    """Return raw address from the house's HTML."""
    raw_address = house_html.find('h2', class_='search-result__header-title').text
    return clean_address(raw_address)


def parse_price(house_html: bs4.BeautifulSoup) -> int:
    """Return the parsed price in euros."""
    raw_price = house_html.find('span', class_='search-result-price').text
    return clean_price(raw_price)


def clean_address(raw_address: str) -> str:
    """Return the cleaned address."""
    return raw_address.strip()


def clean_price(raw_price: str) -> int:
    """Clean the address, parse it and return it as an integer."""
    return int(raw_price.replace('€ ', '')
                        .replace(' k.k.', '')
                        .replace(' v.o.n.', '')
                        .replace('Price on request', '0')
                        .replace('.', '')
                        .replace(',', ''))
