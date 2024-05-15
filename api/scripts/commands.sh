#!/bin/bash

echo "Iniciando o gerenciador de migrações do Alembic."

# Argumento passado para o script
COMMAND=$1

case $COMMAND in
  "upgrade")
    echo "Atualizando o banco de dados para a versão mais recente..."
    alembic upgrade head
    ;;
  "downgrade")
    echo "Revertendo a última migração..."
    alembic downgrade -1
    ;;
  "revision")
    echo "Criando nova migração..."
    alembic revision --autogenerate -m "$2"
    ;;
  *)
    echo "Comando desconhecido: $COMMAND"
    echo "Comandos válidos: upgrade, downgrade, revision [message]"
    ;;
esac

echo "Operação finalizada."
