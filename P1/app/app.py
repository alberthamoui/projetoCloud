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

# --------------------------- Consultar Dados da API -----------------------------
ALPHA_VANTAGE_API_KEY = "PQPY0AYLGMJD3PTN"  # Insira sua chave da API Alpha Vantage
SYMBOL = "AAPL"  # Símbolo da ação desejada
FUNCTION = "TIME_SERIES_INTRADAY"
INTERVAL = "5min"
ALPHA_VANTAGE_API_URL = f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&interval={INTERVAL}&apikey={ALPHA_VANTAGE_API_KEY}"


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
    try:
        response = requests.get(ALPHA_VANTAGE_API_URL)
        
        # Verifica se a resposta é 403 (problema com o token da API externa)
        if response.status_code == 403:
            logging.error("Erro 403: Token da API Alpha Vantage inválido ou excedeu o limite.")
            raise HTTPException(status_code=403, detail="Token da API Alpha Vantage inválido ou limite excedido.")
        
        response.raise_for_status()  # Levanta exceções para outros códigos HTTP >= 400
        
        data = response.json()
        
        if "Time Series (5min)" in data:
            latest_time = max(data["Time Series (5min)"].keys())
            latest_data = data["Time Series (5min)"][latest_time]
            dados = {
                "symbol": SYMBOL,
                "last_updated": latest_time,
                "open": latest_data["1. open"],
                "high": latest_data["2. high"],
                "low": latest_data["3. low"],
                "close": latest_data["4. close"],
                "volume": latest_data["5. volume"]
            }
        else:
            logging.error("Estrutura de dados inesperada na resposta da API Alpha Vantage.")
            raise HTTPException(status_code=500, detail="Estrutura de dados inesperada na resposta da API.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao consultar a API Alpha Vantage: {e}")
        raise HTTPException(status_code=503, detail="Serviço Alpha Vantage indisponível no momento.")
    
    return JSONResponse(content=dados)

# --------------------------- Deletar Usuários -----------------------------
@app.delete("/delete")
async def delete_all_users():
    users.clear()
    logging.info("Todos os usuários foram deletados.")
    return {"message": "Todos os usuários foram deletados."}