# Use a imagem python como base
FROM python:3.9

# Configure o diretório de trabalho
WORKDIR /app

# Expor a porta que a API vai usar (garantir consistência)
EXPOSE 8000

# Copie os arquivos de requisitos e instale-os
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copie seu código para o container
COPY . .

# Comando para rodar sua aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
