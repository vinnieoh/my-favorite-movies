FROM python:3.12.1-alpine3.19

WORKDIR /src

# Atualizar o apk e instalar dependências adicionais
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Atualizar o pip e instalar dependências
RUN pip install --upgrade pip
COPY ./api/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Configurar variáveis de ambiente
ENV DB_URL='postgresql+asyncpg://postgres:root12345@db:5432/movie'
ENV JWT_SECRET='F3gw2q1CaFfw3M-vwmLvvaU6LUFmFtkDNjrH8PRrg-o'
ENV ALGORITHM='HS256'

# Adicionar api ao PYTHONPATH
ENV PYTHONPATH=/src/api

COPY ./api/ /src/

# Instalar Alembic
RUN pip install alembic

# Copiar script de gerenciamento de migrações
COPY ./api/scripts/alembic_manage.sh /usr/local/bin/alembic_manage.sh
RUN chmod +x /usr/local/bin/alembic_manage.sh

# Criar e configurar o ambiente virtual
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /src/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /src && \
    chmod -R +x /src/scripts && \
    chmod -R 755 /src 

EXPOSE 8000


CMD ["sh", "-c", "/venv/bin/python ./scripts/create_tables_database.py && /venv/bin/python ./main.py"]

