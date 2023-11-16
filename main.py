import os
from urllib.parse import urlencode

import jwt
import requests
from tqdm import tqdm

from config import password, username

BASE_URL = "https://legislacaodestacada.com.br/api/v1"


def log_in():
    url_login = f"{BASE_URL}/auth/login"

    payload_login = {"username": username, "password": password}

    response_login = requests.post(url_login, json=payload_login)

    if response_login.status_code == 201:
        token = response_login.json()["token"]
        print("Login feito! Token ok.")
        return token
    else:
        print("Erro no login.")
        return None


def get_conteudos(token):
    url_conteudos = f"{BASE_URL}/marketplace-produtos/produtosCliente"

    id_usuario = jwt.decode(token, options={"verify_signature": False})["sub"]["_id"]

    params_conteudos = {
        "filtros": '{"value":{"cliente":{"_id":"%s" } } }' % id_usuario,
    }

    response_conteudos = requests.get(url_conteudos, params=urlencode(params_conteudos))

    response_json = response_conteudos.json()

    conteudos = response_json[0]["conteudos"]

    return conteudos


def get_conteudo_programatico(id_conteudo):
    url = f"{BASE_URL}/marketplace-produtos/conteudos/{id_conteudo}"

    response = requests.get(url)

    response_json = response.json()

    return response_json


def download(token, id_conteudo, nomeArquivo, nomeTitulosSumario):
    url = f"{BASE_URL}/conteudos/{id_conteudo}/baixar"

    params_download = {
        "data": '{"nomesArquivos":["%s"], "nomesTitulosSumario": ["%s"] }'
        % (nomeArquivo, nomeTitulosSumario),
    }

    downloaded_file = requests.get(
        url,
        params=urlencode(params_download),
        headers={
            "Authorization": "Bearer %s" % token,
        },
    )

    if downloaded_file.status_code == 200:
        return downloaded_file
    else:
        print(f"Erro ao baixar o arquivo {nomeArquivo}.")


def main():
    token = log_in()
    if not token:
        raise ValueError("Erro no login.")

    conteudos = get_conteudos(token)
    for conteudo in tqdm(conteudos, desc="Conteúdos"):
        conteudo_id = conteudo["_id"]
        nome_conteudo = conteudo["nome"]

        conteudo_programaticos = get_conteudo_programatico(conteudo_id)
        for conteudo_programatico in tqdm(conteudo_programaticos, desc="Arquivos"):
            try:
                parent_node = conteudo_programatico.get("parentNode", "")
                conteudo_arquivo = conteudo_programatico["conteudoArquivo"]
                titulo_arquivo = conteudo_arquivo["titulo"]

                downloaded_file = download(
                    token=token,
                    id_conteudo=conteudo_id,
                    nomeArquivo=conteudo_arquivo["nomeArquivo"],
                    nomeTitulosSumario=conteudo_arquivo["titulo"],
                )

                nome_conteudo = nome_conteudo.replace("/", "-").replace(":", "-")
                parent_node = parent_node.replace("/", "-").replace(":", "-")
                titulo_arquivo = titulo_arquivo.replace("/", "-").replace(":", "-")

                folder_name = os.path.join(nome_conteudo, parent_node)
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                file_name = os.path.join(folder_name, f"{titulo_arquivo}.pdf")

                if downloaded_file is not None:
                    with open(file_name, "wb") as f:
                        f.write(downloaded_file.content)
                else:
                    print(
                        f"Erro no {conteudo_arquivo['nomeArquivo']} falha no download."
                    )

            except KeyError as e:
                print(
                    f"O arquivo {titulo_arquivo} de {folder_name}não foi baixado. Falta a chave: {e}"
                )

    print("Todos os downloads foram concluídos, bons estudos Dr. Mariana!")


if __name__ == "__main__":
    main()
