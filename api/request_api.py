import httpx
from app.config.configs import settings
from app.config.config_redis import redis_repository


AUTHORIZATION = f"Bearer {settings.API_MOVIE}"

BASE_URL = "https://api.themoviedb.org/3/"

headers = {
    "accept": "application/json",
    "Authorization": AUTHORIZATION
}


def request_trading_all_br():
    response = httpx.get(f"{BASE_URL}trending/all/day?language=pt-BR", headers=headers)
    print(response.json())  


request_trading_all_br() 