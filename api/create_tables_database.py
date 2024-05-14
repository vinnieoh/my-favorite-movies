from app.config.configs import settings
from app.config.database import engine
import asyncio
from sqlalchemy.exc import SQLAlchemyError

async def create_tables() -> None:
    # É boa prática manter todas as importações no início do arquivo,
    # a menos que uma importação dinâmica seja necessária por motivos específicos.
    import app.models.__all__models
    
    print('Iniciando a criação das tabelas no banco de dados...')

    async with engine.begin() as conn:
        try:
            # Drop all tables first (comment out if you want to keep existing data)
            await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
            await conn.run_sync(settings.DBBaseModel.metadata.create_all)
            print('Tabelas criadas com sucesso.')
        except SQLAlchemyError as e:
            print(f'Erro ao criar tabelas: {e}')

if __name__ == '__main__':
    asyncio.run(create_tables())
