from bs4 import BeautifulSoup
import requests
from concurrent import futures

base_url = 'https://www.pap.pl'
languages = ['en', 'ru', 'ua']


def prepare_url(url):
    if 'https' in url:
        return url
    else:
        return f"{base_url}{url}"


def parse_pap(subdomain):
    array_of_links = []
    res = requests.get(f'{base_url}/{subdomain}')
    soup = BeautifulSoup(res.text, 'html.parser')
    news_list = soup.find_all('ul', class_='newsList')
    news_found = 0

    if news_list:
        with futures.ThreadPoolExecutor() as executor:
            link_futures = []

            for news in news_list:
                links = news.find_all('a')
                for link in links:
                    link_text = link.text.strip()
                    if len(link_text) > 0:
                        obj = {
                            "title": link_text,
                            "link": prepare_url(link['href']),
                            "article": None
                        }
                        array_of_links.append(obj)
                        link_future = executor.submit(
                            parse_article, link['href'])
                        link_futures.append((link_future, obj))

            for link_future, obj in link_futures:
                article = link_future.result()
                obj['article'] = article
                if article:
                    news_found += 1

    if len(subdomain) > 0 and subdomain not in languages:
        return {
            "page": "page_count",
            "total_pages": "total",
            "news_found": news_found,
            "data": array_of_links
        }
    else:
        return {
            "news_found": news_found,
            "data": array_of_links
        }


def parse_article(link):
    res = requests.get(prepare_url(link))
    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('article', role='article')
    if article:
        image = article.find('img')['src'] if article.find('img') else None
        header = article.find(
            'div', class_='field field--name-field-lead field--type-string-long field--label-hidden field--item').text.strip() if article.find('div', class_='field field--name-field-lead field--type-string-long field--label-hidden field--item') else None
        quote = article.find('blockquote').text.strip(
        ) if article.find('blockquote') else None
        obj = {
            "img": f'{base_url}{image}',
            "header": header,
            "quote": quote
        }
        return obj
