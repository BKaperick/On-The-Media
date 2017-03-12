from lxml import html
import requests

'''All news articles on Washington Post's website have a url
"https://www.washingtonpost.com/[topic]/..."
'''
WaPo_topics = {'world', 'politics', 'news'}


def get_article_data(url):
    '''
    Returns a 2-tuple of plain text from the article, as well as a hash set
    of all linked WaPo articles in the text
    '''
    
    # Create html object
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Get plain text
    article_raw = tree.xpath('//article[@itemprop="articleBody"]//p/text()')
    article_text = ''.join(article_raw)

    suggested = set()
    
    # 'a' nodes seem to hold all external links
    xpath_str = '/html/body/div[@id="pb-root"]/section[@id="main-content"]//a'
    for node in tree.xpath(xpath_str):
        node_url = node.get('href')
        if node_url:
            # Only return internal links to WaPo news articles.
            if any(['washingtonpost.com/' + topic + '/' in node_url for topic in WaPo_topics]):
                suggested.add(node_url)

    return article_text, suggested

# Get list of articles currently on the front page.
r = requests.get('https://newsapi.org/v1/articles?source=the-washington-post&sortBy=top&apiKey=bf235085e456486c962c8afc4b59cd6e')
success = str(r.status_code)
if success != '200':
    raise Exception('error code ' + success)
articles = r.json()['articles']

# Keep track of already-scraped articles
visited = set()

article_urls = [art['url'] for art in articles]
for url in article_urls:
    print(url)
    visited.add(url)
    text, suggested = get_article_data(url)

    # Add to queue the list of urls which have been linked but not already visited
    unexplored = list(suggested - visited)
    article_urls += unexplored

