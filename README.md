# My favorite movies - Projeto de Filmes e Séries Favoritos

## Descrição do Projeto

Este projeto é um sistema de gerenciamento de filmes e séries favoritos, onde os usuários podem adicionar seus filmes e séries preferidos, bem como comentar sobre eles. O sistema consome a API do TMDB para buscar e salvar dados na plataforma. Ele é desenvolvido com FastAPI para o backend e React para o frontend, utilizando PostgreSQL e Redis como bancos de dados.

## Funcionalidades

- Adicionar filmes e séries aos favoritos.
- Adicionar comentários aos filmes e séries.
- Buscar detalhes de filmes e séries na API do TMDB.
- Armazenamento de dados em PostgreSQL.
- Cache utilizando Redis para melhorar o desempenho.

## Tecnologias Utilizadas

- **Backend**: FastAPI
- **Frontend**: React
- **Banco de Dados**: PostgreSQL, Redis
- **API Externa**: The Movie Database (TMDB) API

## Pré-requisitos

- Docker e Docker Compose instalados.
- Criar uma conta na [TMDB](https://www.themoviedb.org/) para obter a API Key.

## Configuração do Ambiente

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Crie o arquivo .env para o backend a partir do exemplo fornecido:
     ```sh
     cp ./api/dotenv_files/.env_exemplo_backend ./api/dotenv_files/.env

3. Edite o arquivo .env e adicione a sua TMDB API Key:
    ```sh
    API_MOVIE=<sua_api_key_da_tmdb>

4. Certifique-se de que o Docker e Docker Compose estão instalados em sua máquina.

    Para iniciar o projeto, utilize o comando:
    ```sh
    docker-compose up --build
     ```
    Este comando irá:

    Construir e iniciar o contêiner do PostgreSQL.

    Construir e iniciar o contêiner do Redis.

    (Comentado) Construir e iniciar o contêiner do backend FastAPI.

    (Comentado) Construir e iniciar o contêiner do frontend React.

    Certifique-se de que todos os serviços estão funcionando corretamente verificando os logs dos contêineres.


## Observações

- Certifique-se de que você possui uma API Key válida da TMDB. Caso não tenha, registre-se no site da TMDB e crie sua key.
- O projeto é configurado para ser executado em contêineres Docker, facilitando a configuração do ambiente e a implantação.
- Para personalizar ou modificar o projeto, edite os arquivos de configuração e o código-fonte conforme necessário.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.