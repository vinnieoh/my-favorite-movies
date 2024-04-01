FROM python:3.11

WORKDIR /src

RUN pip install --upgrade pip
COPY ./api/requirements.txt .

RUN pip install --upgrade pip

#POSTGRE
RUN echo "DB_URL = 'postgresql+asyncpg://postgres:root12345@localhost:5432/movie'" >> .env

#JWT
RUN echo "JWT_SECRET = 'F3gw2q1CaFfw3M-vwmLvvaU6LUFmFtkDNjrH8PRrg-o'" >> .env
RUN echo "ALGORITHM = 'HS256'" >> .env

#RUN pip install --no-cache-dir --upgrade -r  ./backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "./api/main.py"]
#CMD ["python", "./api/main.py", "./backend/create_tables.py"]