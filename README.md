# Projeto Cloud - FastAPI e PostgreSQL

### Nome do Aluno:
Albert David Hamoui

## Descrição do Projeto
Este projeto implementa uma API utilizando FastAPI, com autenticação via JWT e integração com um banco de dados PostgreSQL. A API possui funcionalidades de registro de usuários, login, deletar e consulta a dados financeiros de uma API externa (Alpha Vantage). Além disso, o projeto utiliza Docker para a execução em containers e Docker Compose para facilitar a orquestração.



## Como Executar a Aplicação

### 1. Clone o repositório:
### 2. Navegue até o diretório do projeto:
### 3. Se necessário, crie e ative um ambiente virtual:
### 4. Instale as dependências:
```
pip install -r requirements.txt
```

### 5. Crie um arquivo `.env` com as variáveis de ambiente necessárias:
```
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
DATABASE_URL=postgresql://nome:nome@db:5432/nome
SECRET_KEY= "chave_super_secreta"
```

### 6. Para rodar a aplicação via Docker Compose:
```
docker-compose up -d
```
A aplicação estará disponível em `http://localhost:8000`.

Aqui será possível ver a base de dados criada e os dados inseridos.

### 7. Teste.py:
- Codigo usado para realizar o teste de conexão com o banco de dados
- Só é necessario rodar o codigo para verificar se a conexão foi realizada com sucesso


## Documentação dos Endpoints da API
`POST /registrar`: Registra um novo usuário.

- Requisição: Corpo JSON com os dados do usuário (email, senha).
- Resposta: Um token JWT é gerado ao registrar o usuário.


`POST /login`: Realiza o login do usuário e gera um token JWT.
- Requisição: Corpo JSON com email e senha.
- Resposta: Token JWT.


`GET /consultar`: Consulta as manchetes de notícias do site `The Independent`.
- Requisição: Cabeçalho com token JWT.
- Resposta: Lista de 10 manchetes
`DELETE /delete`: Deleta todos os usuários cadastrados.
- Requisição: Nenhuma.
- Resposta: Mensagem de confirmação.



## Screenshot dos Endpoints Testados
Aqui está a captura de tela dos endpoints testados:
 <!-- colocar imagem aleatoria -->
![Imagem Endpoints](img\endpoints.png)



## Vídeo de Execução da Aplicação
Assista ao vídeo de execução:

[Vídeo de execução](img\videoExecucao.mp4)


## Link para o Docker Hub
A imagem Docker do projeto está disponível no Docker Hub. Você pode usá-la para rodar a aplicação:

https://hub.docker.com/r/alberthamoui/app


## Arquivo Compose
O arquivo compose.yaml está localizado no diretório raiz do projeto. Ele contém a configuração para rodar a aplicação e o banco de dados em containers Docker.


```
📁 P1
├── 📁 app 
│   ├── 📄 app.py
│   ├── 📄 database.py 
│   ├── 📄 models.py 
│   ├── 📄 requirements.txt 
│   ├── 📄 Dockerfile
├── 📁 venv
├── 📄 .gitignore
├── 📄 anotacao.txt
├── 📄 compose.yaml
├── 📄 teste.py
├── 📁 img 
├── 📄endpoins.png
├── 📄 videoExecucao.mp4
📄 README.md
```