from lxml import html
import requests
import pickle
import sys

'''All news articles on Washington Post's website have a url
"https://www.washingtonpost.com/[topic]/..."
'''
WaPo_topics = {'world', 'politics', 'news', 'investigation', 'local'}


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

def name_from_url(url):
    '''
    Extracts a human-readable name to serve as an identifier for each
    unique article.  The urls seem like they may be subject to change.
    '''
    url_data = url.split('.com/')[1]
    url_data = url_data.split('/')
    for i,chunk in enumerate(url_data):
        if len(chunk) == 4 and len(url_data[i+1]) == 2 and len(url_data[i+2]) == 2:
            if '.html' in url_data[i+3]:
                name = url_data[i-1]
            else:
                name = url_data[i+3]
            name.replace('-','_')
            return name
    

# Get list of articles currently on the front page.
r = requests.get('https://newsapi.org/v1/articles?source=the-washington-post&sortBy=top&apiKey=bf235085e456486c962c8afc4b59cd6e')
success = str(r.status_code)
if success != '200':
    raise Exception('error code ' + success)
articles = r.json()['articles']

# Keep track of already-scraped articles
visited = set()
counter = 0

network = dict()

article_urls = [art['url'] for art in articles]
for url in article_urls:
    
    # Scrate data
    text, suggested = get_article_data(url)
    
    # Update information
    name = name_from_url(url)
    network[name] = suggested
    visited.add(name)
    
    # Save text to file
    with open(name + '.txt','w') as f:
        f.write(text)

    # Add to queue the list of urls which have been linked but not already visited
    unexplored = list(suggested - visited)
    article_urls += unexplored
    
    # Periodically save state of scraping
    counter += 1
    print(counter)
    if counter % 10 == 0:
        pickle.dump(visited, file('visited.pkl','wb'))
        pickle.dump(article_urls, file('queue.pkl','wb'))
        pickle.dump(network, file('adj_list.pkl','wb'))
