#!/bin/sh

# Carrega as variáveis de ambiente do arquivo .env
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Verifica se a variável MODEL_NAME está definida
if [ -z "$MODEL_NAME" ]; then
    echo "ERROR: MODEL_NAME not set in .env file."
    exit 1
fi

# Inicia o servidor em segundo plano
echo "Iniciando o servidor..."
ollama serve &

# Verifica se o servidor está ativo
until ollama --version && ollama ps; do
    echo "Aguardando o servidor Ollama iniciar..."
    sleep 1  # Aguarda 1 segundo antes de tentar novamente
done
echo "Servidor iniciado com sucesso."

# Realiza o download do modelo definido no arquivo .env
echo "Puxando o modelo: $MODEL_NAME"
ollama pull "$MODEL_NAME"

# Verifica se o comando foi bem-sucedido
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to pull the model $MODEL_NAME."
    exit 1
fi

echo "Modelo $MODEL_NAME baixado com sucesso."

# Manter o contêiner em execução para que o servidor continue ativo
wait