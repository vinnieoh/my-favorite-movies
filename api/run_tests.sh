#!/bin/bash

# Limpa o banco de dados de teste
echo "Limpando o banco de dados de teste..."
python ./scripts/tests_create_tables_database.py

# Executa os testes
echo "Executando os testes..."
PYTHONPATH=./api pytest --disable-warnings --maxfail=1
#PYTHONPATH=./api pytest

echo "Limpando o banco de dados de teste..."
python ./scripts/tests_create_tables_database.py