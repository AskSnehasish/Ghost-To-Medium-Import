from bs4 import BeautifulSoup
import requests
import sys
import json

# URL of the sitemap provided as input from Node.js script
sitemap_url_from_node = ''

# Get data from stdin
# for line in sys.stdin:
#     sitemap_url_from_node = json.loads(line.strip())[0]

def extract_urls_from_sitemap_url(sitemap_url):
    """
    Function to extract all URLs listed in a sitemap.

    Parameters:
    sitemap_url (str): The URL of the sitemap.

    Returns:
    list: A list of URLs extracted from the sitemap.
    """
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')

    urls = [loc.text for loc in soup.find_all('loc') if loc]

    return urls

def get_post_category_by_visiting_url(url):
    print(url)
    """
    Function to extract the category of a post by visiting its URL.

    Parameters:
    url (str): The URL of the post.

    Returns:
    str: The category of the post.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.find('a', {'class': 'post-tag'}).text)
    category = soup.find('a', {'class': 'post-tag'}).text

    return category

def categorize_urls_based_on_text_in_it(url):
    """
    Function to categorize URLs based on the text in them.

    Parameters:
    url (str): The sitemap URL containing the URLs to be categorized.

    Returns:
    list: A list of dictionaries, each containing a URL and its associated category.
    """
    urls = extract_urls_from_sitemap_url(url)
    categorized_urls = []
    
    for url in urls:
        post_category = get_post_category_by_visiting_url(url)
        categorized_url = {
            'url': url,
            'category': post_category
        }
        categorized_urls.append(categorized_url)
    
    return categorized_urls

# Extract and categorize URLs from the sitemap
posts_to_import = categorize_urls_based_on_text_in_it("https://blog.snehasish.dev/sitemap-posts.xml")

# Output the categorized URLs
print(posts_to_import)
