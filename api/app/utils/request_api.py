import json
import httpx
from fastapi import HTTPException
from app.config.configs import settings
from app.config.config_redis import redis_repository


AUTHORIZATION = f"Bearer {settings.API_MOVIE}"

BASE_URL = "https://api.themoviedb.org/3/"

headers = {
    "accept": "application/json",
    "Authorization": AUTHORIZATION
}


def request_trading_all_week_br():
    
    cache_key = "trending_all_week_br"
    url = f"{BASE_URL}trending/all/week?language=pt-BR"
    
    cached_data = redis_repository.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data) 
    
    response = httpx.get(url, headers=headers)
    
    if response.is_success:
        data = response.json()
        redis_repository.insert(cache_key, data)
        return data
        
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")
    

def request_trading_all_day_br():
    cache_key = "trending_all_day_br"
    url = f"{BASE_URL}trending/all/day?language=pt-BR"
    
    cached_data = redis_repository.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data) 
    
    response = httpx.get(url, headers=headers)
    
    if response.is_success:
        data = response.json()
        redis_repository.insert(cache_key, data)
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")
    


def request_search_conteudo(conteudo: str):
    cache_key = f"search_{conteudo}"
    url = f"{BASE_URL}search/multi?query={conteudo}&include_adult=false&language=pt-BR&page=1"
    
    cached_data = redis_repository.get(cache_key)
    
    if cached_data:
        return cached_data
    
    response = httpx.get(url, headers=headers)
    
    if response.is_success:
        data = response.json()
        redis_repository.insert(cache_key, data)
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")
   

def request_movie_id(id: int):
    cache_key = f"movie_{id}"
    url = f"{BASE_URL}movie/{id}?language=pt-BR"
    
    cached_data = redis_repository.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    response = httpx.get(url, headers=headers)
    
    if response.is_success:
        data = response.json()
        redis_repository.insert(cache_key, data)
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")


def request_tv_show_id(id: int):
    cache_key = f"tv_show_{id}"
    url = f"{BASE_URL}tv/{id}?language=pt-BR"
    
    cached_data = redis_repository.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    response = httpx.get(url, headers=headers)
    
    if response.is_success:
        data = response.json()
        redis_repository.insert(cache_key, data)
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")