import ryan_tools as rt
import requests
from bs4 import BeautifulSoup
import os

def get_article_urls():
    sitemap = requests.get('https://www.graphicproducts.com/xmlsitemap/')
    text = sitemap.text
    text = text.replace('\t', '')
    text = text.split('\n')
    final = []
    for item in text:
        if ('loc' in item) and ('.com/articles' in item):
            final.append(item.replace('<loc>', '').replace('</loc>', ''))
            
    return final


def parse_article(article):
    result = article.find_all(["h1", "h2", "h3", "h4", "h5", "h6", 'p'])
    return result


def get_article_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.find_all('article')
    
    article_list = []
    
    
    for article in articles:
        article_list.append(parse_article(article))
    return article_list

os.chdir('data')
url_list = get_article_urls()
i = 0
bar = rt.progress_bar(len(url_list))
for url in url_list:
    if url != 'https://www.graphicproducts.com/articles/':
        name = url.split('articles/')[1]
        name = name.replace('/', '')
        name = name + '.txt'

        if not os.path.exists(name):
            articles = get_article_list(url)
            if len(articles) > 0:
                article = articles[0]
                text = str(article)
                with open('{}'.format(name), 'w') as f:
                    f.write(str(text))
                    i = i + 1

    bar.progress()


