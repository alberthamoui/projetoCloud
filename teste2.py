import os
import uuid
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def unique_email():
    return f"usuarioCloud+{uuid.uuid4().hex}@insper.edu.br"


def test_register_login_consultar_flow():
    # 1) Registrar com email único (evita conflito 409 em execuções repetidas)
    email = unique_email()
    senha = "senhaDoUsuarioCloud"

    register_data = {
        "nome": "Disciplina Cloud",
        "email": email,
        "senha": senha,
    }

    r = requests.post(f"{BASE_URL}/registrar", json=register_data, timeout=10)
    assert r.status_code in (200, 201), f"Registro falhou: {r.status_code} {r.text}"

    reg_json = r.json()
    assert "token" in reg_json and reg_json["token"], "Registro não retornou token"
    assert "user" in reg_json and reg_json["user"]["email"] == email

    # 2) Login
    login_data = {"email": email, "senha": senha}
    r = requests.post(f"{BASE_URL}/login", json=login_data, timeout=10)
    assert r.status_code == 200, f"Login falhou: {r.status_code} {r.text}"

    login_json = r.json()
    token = login_json.get("token")
    assert token, "Login não retornou token"

    # 3) Consultar (endpoint protegido)
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/consultar", headers=headers, timeout=20)

    # Aqui pode variar dependendo do seu código:
    # - Se estiver tudo ok, deve ser 200 e JSON com 'headlines'
    # - Se o site externo falhar, seu endpoint pode retornar erro.
    assert r.status_code == 200, f"/consultar falhou: {r.status_code} {r.text}"

    data = r.json()
    assert "headlines" in data, f"Resposta inesperada de /consultar: {data}"
    assert isinstance(data["headlines"], list), "headlines não é lista"


def test_consultar_requires_auth():
    """GET /consultar sem header Authorization deve retornar 401."""
    r = requests.get(f"{BASE_URL}/consultar", timeout=10)
    assert r.status_code == 401, f"Esperado 401 sem auth, veio {r.status_code}: {r.text}"


def test_login_invalid_credentials():
    """Login com email/senha inexistentes deve retornar 401."""
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": "naoexiste@insper.edu.br", "senha": "senhaerrada"},
        timeout=10,
    )
    assert r.status_code == 401, f"Esperado 401 para credenciais inválidas: {r.status_code} {r.text}"


def test_consultar_invalid_token():
    """GET /consultar com token inválido deve retornar 401."""
    r = requests.get(
        f"{BASE_URL}/consultar",
        headers={"Authorization": "Bearer token_invalido_123"},
        timeout=10,
    )
    assert r.status_code == 401, f"Esperado 401 para token inválido: {r.status_code} {r.text}"

def test_register_duplicate_email_returns_409():
    email = unique_email()
    payload = {"nome": "Dup", "email": email, "senha": "123"}

    r1 = requests.post(f"{BASE_URL}/registrar", json=payload, timeout=10)
    assert r1.status_code in (200, 201)

    r2 = requests.post(f"{BASE_URL}/registrar", json=payload, timeout=10)
    assert r2.status_code == 409, f"Esperado 409 para email duplicado: {r2.status_code} {r2.text}"


def test_registrar_invalid_email_returns_422():
    r = requests.post(
        f"{BASE_URL}/registrar",
        json={"nome": "X", "email": "email-invalido", "senha": "123"},
        timeout=10,
    )
    assert r.status_code == 422, f"Esperado 422 para email inválido: {r.status_code} {r.text}"


def test_login_missing_field_returns_422():
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": "alguem@insper.edu.br"},  # falta senha
        timeout=10,
    )
    assert r.status_code == 422, f"Esperado 422 para payload inválido: {r.status_code} {r.text}"


def test_consultar_malformed_authorization_returns_401():
    # sem Bearer
    r = requests.get(
        f"{BASE_URL}/consultar",
        headers={"Authorization": "Token abc"},
        timeout=10,
    )
    assert r.status_code == 401, f"Esperado 401 para Authorization malformado: {r.status_code} {r.text}"


def test_delete_clears_users():
    email = unique_email()
    senha = "123"
    requests.post(
        f"{BASE_URL}/registrar",
        json={"nome": "ToDelete", "email": email, "senha": senha},
        timeout=10,
    )

    r = requests.delete(f"{BASE_URL}/delete", timeout=10)
    assert r.status_code == 200, f"DELETE /delete falhou: {r.status_code} {r.text}"

    # depois de apagar, login deve falhar
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "senha": senha},
        timeout=10,
    )
    assert r.status_code == 401, f"Esperado 401 após delete: {r.status_code} {r.text}"
