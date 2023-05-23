# PAP open-api

PAP open-api is simple scraper of PAP.PL (Polska Agencja Prasowa). Script will parse the page and return  clean api. Code uses multithreading for faster scraping.

## Run

Use the package manager [pip](https://pip.pypa.io/en/stable/) to run scraper.

```bash
pip install -r requirements.txt
```
```bash
cd src/api && uvicorn main:app --reload
```

## Usage

After running server (second command) you can navigate to:

```
http://127.0.0.1:8000/
```
and you will see that informations:

```json
{
  "message": "Hi, you're using PAP open-api. Down below there is short info about usage.",
  "languages": {
    "PL": [
      "/api",
      "PATHS"
    ],
    "EN": [
      "/api/en/world",
      "/api/en/business"
    ],
    "UA": [
      "/api/ua"
    ],
    "RU": [
      "/api/ru"
    ]
  },
  "paths": [
    "/api/kraj",
    "/api/swiat",
    "/api/gospodarka",
    "/api/sport",
    "/api/nauka",
    "/api/kultura",
    "/api/zdrowie",
    "/api/przeglad-mediow"
  ]
}
```

  > /api - parse main page (latest news/ articles)

Example news object:

```json
{
  "title": "Title of the article",
  "link": "Web url to the article",
  "article": {
    "img": "Web url to the image of the article",
    "date": "Date and last update",
    "header": "Header of the article",
    "quote": "Full article"
  }
}
```



## License

[MIT](https://choosealicense.com/licenses/mit/)
