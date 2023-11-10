import os
import requests
from config import username, password

def log_in():
    url_login = "https://legislacaodestacada.com.br/api/v1/auth/login"
    payload_login = f'{{"username":"{username}","password":"{password}"}}'
    headers_login = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://legislacaodestacada.com.br",
        "Referer": "https://legislacaodestacada.com.br/auth/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua": "^Google",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "^Android",
        "Authorization": "Bearer ",
    }

    response_login = requests.post(url_login, data=payload_login, headers=headers_login)

    if response_login.status_code == 201:
        token = response_login.json()["token"]
        print("Login feito! Token ok.")
        return token
    else:
        print("Erro no login.")
        return None

def download(token, num_dias, nome_pasta):
    for variavel in range(num_dias + 1):
        url_download = "https://legislacaodestacada.com.br/api/v1/conteudos/6425a420c8c0a8dc4bd652f2/baixar"

        querystring = {
            "data": f'{{"label":"baixarUnico-col:1","conteudoId":"64dd0a0e7ee0b7c1644c3ce3","nomesArquivos":["PLANO-COMPLEMENTAR-TJGO-PO-S-EDITAL-DIA-{variavel}"],"analise":false,"index":{variavel},"nomesTitulosSumario":["DIA {variavel}"],"nomeCliente":"Mariana Valentim","cpf":"08519527981"}}',
        }

        headers_download = {
            "User-Agent": "insomnia/8.3.0",
            "Authorization": f"Bearer {token}"
        }

        response_download = requests.get(url_download, headers=headers_download, params=querystring)

        if response_download.status_code == 200:
            with open(os.path.join(nome_pasta, f"DIA {variavel}.pdf"), "wb") as f:
                f.write(response_download.content)
            print(f"Arquivo DIA {variavel}.pdf baixado.")
        else:
            print(f"Erro ao baixar o arquivo DIA{variavel}.pdf.")

def main():
    token = log_in()

    if token:
        print('Coloque o número de dias do curso:')
        num_dias = int(input())
        nome_pasta = input('Coloque o nome da pasta:')

        if not os.path.exists(nome_pasta):
            os.mkdir(nome_pasta)

        download(token, num_dias, nome_pasta)

        print("Todos os downloads foram concluídos, bons estudos Dr.Mariana!")

if __name__ == "__main__":
    main()
