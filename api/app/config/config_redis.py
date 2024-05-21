from redis import Redis
import json

from app.config.configs import settings


class RedisConnectionHandle:
    def __init__(self) -> None:
        self.__host = settings.HOST_REDIS
        self.__port = settings.PORT_REDIS
        self.__db = settings.DB_REDIS
        self.__connection = None
    
    def connect(self) -> Redis:
        self.__connection = Redis(
            host=self.__host,
            port=self.__port,
            db=self.__db
        )
        
        return self.__connection
    
    def get_conn(self) -> Redis:
        return self.__connection


__redis_connection = RedisConnectionHandle().connect()


class RedisRepository:
    def __init__(self, redis_conn: Redis) -> None:
        self.__redis_conn = redis_conn
    
    def get(self, key: str) -> any:
        value = self.__redis_conn.get(key)
        
        if value:
            return value.decode('utf-8')
        return None

    def insert_hash(self, key: str, field: str, value: any) -> None:
        self.__redis_conn.hset(key, field, value)

    def get_hash(self, key: str, field: str) -> any:
        value = self.__redis_conn.hget(key, field)
        
        if value:
            return value.decode('utf-8')
        return None

    def insert(self, key: str, value: any, ex: int = settings.REDIS_EXPIRATION_TIME_24H) -> None:
        value = json.dumps(value)
        self.__redis_conn.set(key, value, ex=ex)

    def insert_hash_ex(self, key: str, field: str, value: any, ex: int = settings.REDIS_EXPIRATION_TIME_24H) -> None:
        self.__redis_conn.hset(key, field, value)
        self.__redis_conn.expire(key, ex)
        
        
redis_repository = RedisRepository(__redis_connection)