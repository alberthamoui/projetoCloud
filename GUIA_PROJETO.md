
# Guia Único e Completo — API Docker AWS (Projeto P1)

RESUMO:

cd P1
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r app\requirements.txt
cd app
..\venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
P1\venv\Scripts\python.exe -m pytest teste2.py -v

cd P1
docker compose up --build -d
P1\venv\Scripts\python.exe -m pytest teste2.py -v
docker compose down



No modo AWS, eu não rodo a API manualmente. O Kubernetes cria os containers a partir das imagens, 
expõe a API via Load Balancer, e eu interajo como cliente usando a URL pública.

Terminal 1 cria o cluster, Terminal 2 sobe os containers no Kubernetes, Terminal 3 descobre a URL pública, Terminal 4 testa a API como cliente.
---

## 1) O que o projeto faz

API em **FastAPI** com:
- Autenticação **JWT** (tokens gerados em `/registrar` e `/login`)
- Endpoint protegido `/consultar` que retorna até **10 manchetes** do site **The Independent**
- Usuários armazenados **em memória** (`users = []`), para simplificar o demo
- Endpoint administrativo `/delete` para limpar a lista de usuários

Endpoints principais:
- `POST /registrar` → registra usuário e devolve token JWT
- `POST /login` → autentica e devolve token JWT
- `GET /consultar` → protegido (exige token), retorna manchetes
- `DELETE /delete` → apaga todos usuários (memória)
- `GET /teste` → healthcheck simples (`{"teste":"ok"}`)
- `GET /` → retorna `{"users": [...]}` (debug)

---

## 2) Estrutura do repositório (P1)

```
P1/
├── app/
│   ├── app.py              # FastAPI, JWT, rotas, scraping
│   ├── database.py         # users = [] (memória)
│   ├── models.py           # Pydantic models (User, Login, UserList, Consult)
│   ├── Dockerfile          # imagem do app (uvicorn app:app)
│   └── requirements.txt
├── compose.yaml            # FastAPI + Postgres via Docker Compose
├── deployment.yml          # Kubernetes Deployment (FastAPI)
├── postgres-deployment.yml # Kubernetes Deployment (Postgres)
├── service.yml             # Kubernetes Services (LoadBalancer + ClusterIP)
├── teste.py                # teste manual (requests)
└── venv/                   # ambiente local (opcional)
```

---

## 3) Fluxo de uso da API (o que demonstrar)

### 1. Registrar
`POST /registrar`
```json
{"nome":"...", "email":"...", "senha":"..."}
```

Resposta:
```json
{"user": {...}, "token": "<jwt>"}
```

### 2. Colocar o token no Swagger
- Abrir `/docs`
- Clicar **Authorize**
- Colar o token JWT
- Authorize / Close

### 3. Consultar (protegido)
`GET /consultar`
```json
{"headlines": ["...", "...", ...]}
```

---

## 4) Execução sem Docker (Local)

### Pré-requisitos
- Python 3.9+

### Setup
```powershell
cd P1
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r app\requirements.txt
```

### Variáveis de ambiente
`P1\app\.env`
```
SECRET_KEY=chave_super_secreta_local_com_32_ou_mais_caracteres
```

### Subir API
```powershell
cd P1\app
..\venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Swagger: http://127.0.0.1:8000/docs

---

## 5) Execução com Docker

### Pré-requisitos
- Docker + Docker Compose

### Variáveis
`P1\.env`
```
POSTGRES_DB=project
POSTGRES_USER=project
POSTGRES_PASSWORD=project
DATABASE_URL=postgresql://project:project@db:5432/project
SECRET_KEY=chave_super_secreta_docker_com_32_ou_mais_caracteres
```

### Subir
```powershell
cd P1
docker compose up --build -d
```

Swagger: http://localhost:8000/docs

### Parar
```powershell
docker compose down
```

---

## 6) Validação oficial (pytest)

```powershell
cd <raiz-do-repositorio>
$env:BASE_URL='http://127.0.0.1:8000'
P1\venv\Scripts\python.exe -m pytest teste2.py -v
```

---

## 7) AWS / EKS (explicação conceitual)

Arquivos Kubernetes:
- `deployment.yml` → Deployment da FastAPI
- `postgres-deployment.yml` → Deployment do Postgres
- `service.yml` → Services (Postgres interno + FastAPI LoadBalancer)

Fluxo:
1. Criar cluster EKS
2. Configurar `kubectl`
3. `kubectl apply -f ...`
4. Obter `EXTERNAL-IP`
5. Acessar `/docs` pelo Load Balancer

Frase pronta:
> “O deploy foi feito em conta educacional da faculdade; mantenho os manifests no repositório, mas hoje não tenho acesso à conta para reproduzir ao vivo.”

---