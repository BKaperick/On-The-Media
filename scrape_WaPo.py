from lxml import html
import requests

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
    # Skips over some nodes in final depth search
    #xpath_str = '/html/body/div[@id="pb-root"]/section[@id="main-content"]/div[@class="moat-trackable pb-f-theme-normal full pb-feature pb-layout-item pb-f-page-recommended-strip"]/div[@id="post-recommends"]/div[@id="slug_postrecommends"]'
    
    #xpath_str = '/html/body/div[@id="pb-root"]/section[@id="main-content"]/div[@class="moat-trackable pb-f-theme-normal full pb-feature pb-layout-item pb-f-page-recommended-strip"]/div[@id="post-recommends"]/div[@class="postrecommends contentfeed"]/div[@class="content-strip"]/div[4]/div/div/div[2]/div[2]/a'
    #xpath_str = '////div[class="content-strip"]'
    xpath_str = '/html/body/div[@id="pb-root"]/section[@id="main-content"]//a'
    sugg = tree.xpath(xpath_str)
    for sugg_obj in sugg:
        sugg_url = sugg_obj.get('href')
        if sugg_url:
            if any(['washingtonpost.com/' + x + '/' in sugg_url for x in WaPo_topics]):
                suggested.add(sugg_url)

    return article_text, suggested

r = requests.get('https://newsapi.org/v1/articles?source=the-washington-post&sortBy=top&apiKey=bf235085e456486c962c8afc4b59cd6e')
print(r.status_code)
articles = r.json()['articles']

visited = set()
art = articles[0]
#for art in articles:
url = art['url']
visited.add(url)
text, suggested = get_article_data(url)
#print(text)
#print(suggested)
