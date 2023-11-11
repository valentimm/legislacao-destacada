import os
from urllib.parse import urlencode

import jwt
import requests

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
    """
    https://legislacaodestacada.com.br/api/v1/marketplace-produtos/produtosCliente?filtros=%7B%22value%22:%7B%22cliente%22:%7B%22_id%22:%22645d7c3526d358cfbfc57b98%22,%22nome%22:%22Mariana%20Valentim%22,%22email%22:%22mariana_m_valentim@hotmail.com%22,%22cpf%22:%2208519527981%22,%22celular%22:%2241992482577%22,%22perfil%22:%22CLIENTE%22,%22endereco%22:%7B%22_id%22:%22645d7e38dd05f6d0fcb77418%22,%22logradouro%22:%22Alameda%20J%C3%BAlia%20da%20Costa%22,%22numero%22:%222102%22,%22complemento%22:%22Apartamento%20203%22,%22cep%22:%2280730-070%22,%22bairro%22:%22Bigorrilho%22,%22municipio%22:%22Curitiba%22,%22localidade%22:%22Curitiba%22,%22uf%22:%22PR%22%7D,%22ativo%22:true,%22senha%22:%22$2a$10$bK6V6OljrKper/44vLiQKe67ifjSZ.lrc6/0IQNvwh0HtoIqbw4si%22,%22contatos%22:%5B%5D,%22createdAt%22:%222023-05-11T23:37:25.965Z%22,%22updatedAt%22:%222023-05-11T23:46:00.961Z%22,%22__v%22:0,%22dataNascimento%22:%221997-04-13T03:00:00.000Z%22,%22imagem%22:%22http://legislacaodestacada.com.br/images/usuarios/profile.jpg%22,%22sexo%22:%22MASCULINO%22%7D%7D%7D
    """
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
    for conteudo in conteudos:
        conteudo_id = conteudo["_id"]
        nome_conteudo = conteudo["nome"]

        conteudo_programaticos = get_conteudo_programatico(conteudo_id)
        for conteudo_programatico in conteudo_programaticos:
            parent_node = conteudo_programatico.get("parentNode", "")
            conteudo_arquivo = conteudo_programatico["conteudoArquivo"]
            titulo_arquivo = conteudo_arquivo["titulo"]

            downloaded_file = download(
                token=token,
                id_conteudo=conteudo_id,
                nomeArquivo=conteudo_arquivo["nomeArquivo"],
                nomeTitulosSumario=conteudo_arquivo["titulo"],
            )

            folder_name = os.path.join(nome_conteudo, parent_node)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_name = os.path.join(folder_name, f"{titulo_arquivo}.pdf")
            with open(file_name, "wb") as f:
                f.write(downloaded_file.content)

    print("Todos os downloads foram concluídos, bons estudos Dr.  Mariana!")


if __name__ == "__main__":
    main()
