# Usando a imagem oficial do Redis do Docker Hub
FROM redis:latest

# Mantém o proprietário do container como root
USER root

# Define a porta que o Redis irá expor
EXPOSE 6379

# Comando para rodar o Redis no modo padrão (não como daemon)
CMD ["redis-server"]

# Você pode adicionar configurações personalizadas do Redis copiando um arquivo de configuração
# COPY redis.conf /usr/local/etc/redis/redis.conf

# E usar o comando abaixo para iniciar o Redis com a configuração personalizada
# CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
