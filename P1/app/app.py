from fastapi import FastAPI, HTTPException, Depends, APIRouter, Header
from fastapi.security import OAuth2PasswordBearer
from models import User, Login, Consult, UserList
from database import users
import logging
import requests
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup


app = FastAPI()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")




# --------------------------- JWT -----------------------------
def create_jwt_token(user):
    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")


# --------------------------- Logging -----------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --------------------------- Registrar API Router -----------------------------
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(router)

@app.get("/")
def read_root():
    return {"users": users}


@app.get("/teste") 
def read_root():
    return {"111111111111111111111": []}

# --------------------------- Registrar Usuários -----------------------------
@app.post("/registrar")
async def create_user(user: User):
    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=409, detail="Email já cadastrado.")
    users.append(user)
    token = create_jwt_token(user)
    logging.info("Usuário registrado com sucesso!")
    return {"user": user, "token": token}

@app.post("/registrar_muitos")
async def create_multiple_users(user_list: UserList):
    added_users = []
    for user in user_list.users:
        for existing_user in users:
            if existing_user.email == user.email:
                raise HTTPException(status_code=409, detail=f"Email já cadastrado: {user.email}")
        users.append(user)
        token = create_jwt_token(user)
        added_users.append({"user": user, "token": token})

    logging.info("Vários usuários registrados com sucesso!")
    return {"added_users": added_users}

# --------------------------- Login -----------------------------
@app.post("/login")
async def login(login: Login):
    for user in users:
        if user.email == login.email and user.senha == login.senha:
            token = create_jwt_token(user)
            logging.info(f"Login realizado com sucesso para o usuário: {user.email}")
            return {"user": user, "token": token}
    raise HTTPException(status_code=401, detail="Credenciais inválidas.")


# --------------------------- Deletar Usuários -----------------------------
@app.delete("/delete")
async def delete_all_users():
    users.clear()
    logging.info("Todos os usuários foram deletados.")
    return {"message": "Todos os usuários foram deletados."}


# --------------------------- Consultar Dados da API -----------------------------
@app.get("/consultar", response_model=Consult)
def get_user(authorization: str = Header(None, alias="Authorization")):
    if not authorization:
        raise HTTPException(status_code=401, detail="Credenciais não fornecidas (not authorization).")
    if "Bearer " not in authorization:
        raise HTTPException(status_code=401, detail="Credenciais incompatíveis (Sem Bearer).")
    
    token = authorization.split(" ")[1]
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Credenciais inválidas (Sem payload).")

    # --------------------------- Consulta API Alpha Vantage -----------------------------
    # Define the headers to mimic a request from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send a GET request to The Independent's homepage
    url = "https://www.independent.co.uk/"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from The Independent."}

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the headlines (you may need to adjust this selector based on the site's structure)
    headlines = []
    for headline in soup.find_all("h2"):
        text = headline.get_text(strip=True)
        if text:
            headlines.append(text)

    return {"headlines": headlines[:10]}
