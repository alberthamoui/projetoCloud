# Projeto Cloud - FastAPI e PostgreSQL

### Nome do Aluno:
Albert David Hamoui

## Descrição do Projeto
Este projeto implementa uma API utilizando **FastAPI**, com autenticação via **JWT** e integração com um banco de dados **PostgreSQL**. A API oferece funcionalidades para registro e autenticação de usuários, além de consultas a notícias de um site externo (**The Independent**). O projeto também utiliza **Docker** para containerização e **Docker Compose** para orquestração.

## Como Executar a Aplicação

### Pré-requisitos
- Docker e Docker Compose instalados.
- Clonar este repositório:
  ```bash
  git clone https://github.com/alberthamoui/projetoCloud.git
  ```
- Navegar até o diretório do projeto:
  ```bash
  cd <nome-do-diretorio>
  ```

### Configuração
#### 1. Crie um arquivo `.env` com as variáveis de ambiente necessárias:
    ```bash
    POSTGRES_DB=nome_do_banco
    POSTGRES_USER=usuario
    POSTGRES_PASSWORD=senha
    DATABASE_URL=postgresql://nome:nome@db:5432/nome
    SECRET_KEY="chave_super_secreta"
    ```


#### 2. Execute o projeto com Docker Compose:
    ```bash
    docker-compose up -d
    ```

### Uso da Aplicação
#### 1. Acesse a aplicação em `http://localhost:8000`.
#### 2. Utilize as rotas da API conforme a documentação abaixo.
#### 3. Extra: Para testar a conexão com o banco de dados, execute o arquivo `teste.py`.


---

## Documentação dos Endpoints da API
### `POST /registrar`
- **Descrição:** Registra um novo usuário.
- **Entrada:** JSON com `email` e `senha`.
- **Saída:** Token JWT gerado para o usuário registrado.

### `POST /login`
- **Descrição:** Autentica o usuário e retorna um Token JWT.
- **Entrada:** JSON com `email` e `senha`.
- **Saída:** Token JWT.

### `GET /consultar`
- **Descrição:** Retorna as manchetes de notícias do site *The Independent*.
- **Cabeçalho necessário:** Token JWT no formato `Bearer <token>`.
- **Saída:** Lista de 10 manchetes.

### `DELETE /delete`
- **Descrição:** Deleta todos os usuários cadastrados.
- **Entrada:** Nenhuma.
- **Saída:** Mensagem de confirmação.

---

## Screenshot dos Endpoints Testados
Aqui está uma captura de tela com os testes realizados:

![Imagem Endpoints Testados](img/endpoints.png)

---

## Vídeo de Execução da Aplicação
Veja o vídeo demonstrativo da execução do projeto:
[Vídeo de Execução](img/videoExecucao.mp4)

---

## Link para o Docker Hub
A imagem Docker do projeto está disponível no Docker Hub:  
[Docker Hub - alberthamoui/app](https://hub.docker.com/r/alberthamoui/app)

---

## Arquivo Compose
O arquivo `compose.yaml` está localizado na raiz do projeto. Ele contém as definições necessárias para rodar os containers da aplicação e do banco de dados. O arquivo utiliza apenas imagens do **Docker Hub**, como exigido.

---

### Estrutura do Repositório
```bash
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
├── 📄 endpoins.png
├── 📄 videoExecucao.mp4
📄 README.md
```