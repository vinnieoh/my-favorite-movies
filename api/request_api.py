import httpx
from app.config.configs import settings
from app.config.config_redis import redis_repository


AUTHORIZATION = f"Bearer {settings.API_MOVIE}"

BASE_URL = "https://api.themoviedb.org/3/"

headers = {
    "accept": "application/json",
    "Authorization": AUTHORIZATION
}


def request_trading_all_week_br():
    
    url = f"{BASE_URL}trending/all/week?language=pt-BR"
    
    response = httpx.get(url, headers=headers)
    
    print(response.json())  


def request_trading_all_day_br():
    
    url = f"{BASE_URL}trending/all/day?language=pt-BR"
    
    response = httpx.get(url, headers=headers)
    
    print(response.json()) 


def request_search_conteudo(conteudo = 'scarface'):
    
    url = f"{BASE_URL}search/keyword?query={conteudo}&page=1"
    
    response = httpx.get(url, headers=headers)
    print(response.json())
   

def request_find_by_id(id: int =  10):
    
    url = f"{BASE_URL}collection/{id}??language=pt-BR"
    
    response = httpx.get(url, headers=headers)
    print(response.json())


def request_movie_id(id = 11):
    
    url = f"{BASE_URL}tv/{id}?language=pt-BR"
    
    response = httpx.get(url, headers=headers)
    print(response.json())


def request_tv_show_id(id):
    url = f"{BASE_URL}movie/{id}?language=pt-BR"
    
    response = httpx.get(url, headers=headers)
    print(response.json())


def request_():
    
    url = f"{BASE_URL}"
    
    response = httpx.get(url, headers=headers)
    print(response.json())


def request_():
    
    url = f"{BASE_URL}"
    
    response = httpx.get(url, headers=headers)
    print(response.json())




##################################################################

#request_search_conteudo()

#request_trading_all_day_br()

#request_trading_all_week_br()

#request_find_by_id()

request_movie_id()