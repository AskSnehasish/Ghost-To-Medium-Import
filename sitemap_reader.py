import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import sys
import json

ghost_cms_sitemap = ''
# Get data from stdin
for line in sys.stdin:
    ghost_cms_sitemap = json.loads(line.strip())[0]

def extract_urls_from_sitemap_url(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')

    urls = []
    for url in soup.find_all('url'):
        loc = url.find('loc')
        if loc is not None:
            urls.append(loc.text)

    return urls

def get_post_category_by_visiting_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category = soup.find('a', {'class': 'post-tag'}).text
    return category

def categorize_urls_based_on_text_in_it(url):
    urls = extract_urls_from_sitemap_url(url)
    new_urls = []
    for url in urls:
        post_category = get_post_category_by_visiting_url(url)
        new_url = {}
        new_url['url'] = url
        new_url['category'] = post_category
        new_urls.append(new_url)
    return new_urls

posts_to_import = categorize_urls_based_on_text_in_it(ghost_cms_sitemap)
print(posts_to_import)