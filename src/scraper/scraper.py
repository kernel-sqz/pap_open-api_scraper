from bs4 import BeautifulSoup
import requests
import json


base_url = 'https://www.pap.pl'


def custom_encoder(obj):
    if isinstance(obj, str):
        return obj.encode('unicode_escape').decode()
    return obj


def parse_pap():
    array_of_links = []
    res = requests.get(base_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    div = soup.find('div', class_='newsWrapper')

    if div:
        links = div.find_all('a')
        for link in links:

            if len(link.text.strip()) > 0:
                array_of_links.append({
                    "title": link.text.strip(),
                    "link": f"{base_url}{link['href']}",
                    "article": parse_article(link['href'])
                })
    print(json.dumps(array_of_links, ensure_ascii=False,
          default=custom_encoder, indent=4))


def parse_article(link):
    res = requests.get(f'{base_url}{link}')
    soup = BeautifulSoup(res.content, 'html.parser')
    article = soup.find('article', role='article')
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


parse_pap()
