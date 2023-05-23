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


def parse_pap(subdomain, page):
    link_dict = {}
    res = requests.get(
        f'{base_url}/{subdomain}?page={page}') if subdomain else requests.get(f'{base_url}')
    soup = BeautifulSoup(res.text, 'html.parser')
    news_list = soup.find_all('ul', class_='newsList')
    total_pages = soup.find('a', rel='last')

    news_found = 0

    if news_list:
        with futures.ThreadPoolExecutor() as executor:
            link_futures = []

            for news in news_list:
                links = news.find_all('a')
                for link in links:
                    link_text = link.text.strip()
                    if len(link_text) > 0:
                        link_url = prepare_url(link['href'])
                        if link_url not in link_dict:
                            obj = {
                                "title": link_text,
                                "link": link_url,
                                "article": None
                            }
                            link_dict[link_url] = obj
                            link_future = executor.submit(
                                parse_article, link['href'])
                            link_futures.append((link_future, obj))
                            news_found += 1

            for link_future, obj in link_futures:
                article = link_future.result()
                obj['article'] = article

    unique_links = list(link_dict.values())

    if subdomain and subdomain not in languages:
        prev = f"/api/{subdomain}/?page={page-1}" if page > 0 else ""

        return {
            "page": int(page),
            "next": f"/api/{subdomain}/?page={page+1}",
            "prev": prev,
            "total_pages": int(total_pages['href'].replace('?page=', '')),
            "news_found": int(news_found),
            "data": unique_links
        }
    else:
        return {
            "news_found": news_found,
            "data": unique_links
        }


def parse_article(link):
    res = requests.get(prepare_url(link))
    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.find('article', role='article')

    if article:
        image = article.find('img')['src'] if article.find('img') else None
        date = soup.find('div', class_='moreInfo').text.strip(
        ) if soup.find('div', class_='moreInfo') else None

        header = article.find(
            'div', class_='field field--name-field-lead field--type-string-long field--label-hidden field--item').text.strip() if article.find('div', class_='field field--name-field-lead field--type-string-long field--label-hidden field--item') else None
        quote = article.find('div', property="schema:text").text.strip(
        ).replace('\n', ' ') if article.find('div', property="schema:text") else None
        obj = {
            "img": f'{base_url}{image}',
            "date": date,
            "header": header,
            "quote": quote
        }
        return obj
