from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from .configs import settings

# Criação de um motor assíncrono com a URL do banco de dados extraída das configurações.
# Certifique-se de que a URL está correta e acessível.
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Configuração da factory de sessão para utilizar o modelo assíncrono do SQLAlchemy.
# autocommit=False garante que as transações não serão comitadas automaticamente.
# autoflush=False evita o flush automático das operações para o banco, aumentando o controle sobre as transações.
# expire_on_commit=False mantém os objetos utilizáveis após os commits sem recarregar do banco de dados.
# A sessão é vinculada ao motor criado anteriormente.
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
