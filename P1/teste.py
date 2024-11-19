import requests

# Teste para o Docker
# base_url = 'http://127.0.0.1:8000'

# Teste AWS
base_url = "http://aa8e6d3f34d5343f2a4fa37753f87159-199765277.us-east-2.elb.amazonaws.com"



register_data = {
    "nome": "Disciplina Cloud",
    "email": "usuarioCloud@insper.edu.br",
    "senha": "senhaDoUsuarioCloud"
}

print('Registrar')
print('-' * 50)
response = requests.post(f'{base_url}/registrar', json=register_data)
print(f'Registro - Status Code: {response.status_code}')
print(f'Registro - Resposta: {response.json()}')

login_data = {
    "email": "usuarioCloud@insper.edu.br",
    "senha": "senhaDoUsuarioCloud"
}
print('-' * 50, '\n\n')

print(f'\nLogin')
print('-' * 50)
response = requests.post(f'{base_url}/login', json=login_data)
print(f'Login - Status Code: {response.status_code}')
print(f'Login - Resposta: {response.json()}')

token = response.json().get('token')
print('-' * 50, '\n\n')

print(f'\nConsultar')
print('-' * 50)

print(f'Token: {token}')

if token:
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{base_url}/consultar', headers=headers)
    print(f'Consultar - Status Code: {response.status_code}')
    print(f'Consultar - Conteúdo: {response.text}')  # Mostrar o conteúdo da resposta
    if response.status_code == 200:
        try:
            print(f'Consultar - Resposta: {response.json()}')
        except Exception as e:
            print(f'Erro ao decodificar JSON: {e}')
    else:
        print(f'Erro na consulta, status code: {response.status_code}')
        print(f'Consultar - Resposta: {response.json()}')
else:
    print("Token não recebido.")

print('-' * 50)


