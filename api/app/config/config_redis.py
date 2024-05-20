from redis import Redis

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
        
    def redis_insert(self, key: str, value:any) -> None:
        self.__redis_conn.set(key, value)
        
        
redis_repository = RedisRepository(__redis_connection)