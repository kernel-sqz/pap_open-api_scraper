from fastapi import FastAPI, Query
from scraper.utils import parse_pap

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hi, you're using PAP open-api. Down below there is short info about usage.",
        "languages": {
            "PL": ['/api', "PATHS"],
            "EN": [
                '/api/en/world',
                '/api/en/business'
            ],
            "UA": ["/api/ua"],
            "RU": ["/api/ru"]
        },
        "paths": [
            '/api/kraj',
            '/api/swiat',
            '/api/gospodarka',
            '/api/sport',
            '/api/nauka',
            '/api/kultura',
            '/api/zdrowie',
            '/api/przeglad-mediow',
        ]
    }


@app.get("/api/{subdomain}")
async def root(subdomain: str, page: int = Query(0)):
    return parse_pap(subdomain, page)


@app.get("/api")
async def root():
    return parse_pap(None, None)
