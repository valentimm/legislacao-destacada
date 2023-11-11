import os
import requests
from config import username, password
from data_cleaner import filtered_data

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


def download(token, nome, titulo_arquivo, arquivo):
    for item in filtered_data:
        url_download = "https://legislacaodestacada.com.br/api/v1/conteudos/6283b7388ad7360aa43fadd6/baixar"

        querystring = {
            "data": f'{{"label":"baixarUnico-col:1","conteudoId":"6283b7388ad7360aa43fadd6","nomesArquivos":{titulo_arquivo},"analise":false,"index":1,"nomesTitulosSumario":["DIA 1"],"nomeCliente":"Mariana Valentim","cpf":"08519527981"}}',
        }

        headers_download = {
            "User-Agent": "insomnia/8.3.0",
            "Authorization": f"Bearer {token}"
        }



        response_download = requests.get(url_download, headers=headers_download, params=querystring)

        if response_download.status_code == 200:
            file_name = f"{nome}_{item['some_other_variable']}.pdf"

            with open(os.path.join(arquivo, file_name), "wb") as f:
                f.write(response_download.content)
            print(f"Arquivo {file_name} baixado.")
        else:
            print(f"Erro ao baixar o arquivo {nome}.pdf.")

def main():
    token = log_in()

    if token:
        for item in filtered_data:
            nome_pasta = item['arquivo']

            if not os.path.exists(nome_pasta):
                os.mkdir(nome_pasta)

            download(token, nome_pasta, "seu_titulo_arquivo", "sua_pasta_destino")

        print("Todos os downloads foram concluídos, bons estudos Dr. Mariana!")

if __name__ == "__main__":
    main()
